from pathlib import Path
from time import perf_counter

from app.database.db import db
from app.models.job import Job

from app.parser.apache_parser import ApacheLogParser

from app.detection.detector import ThreatDetector
from app.detection.brute_force import BruteForceDetector

from app.services.aggregation_service import AggregationService
from app.services.log_service import save_logs
from app.services.detection_service import save_detections


class ProcessingService:

    # ---------------------------------------------------------
    # LARGE-FILE PROCESSING SETTINGS
    # ---------------------------------------------------------

    # Logs are relatively lightweight compared with detections,
    # so we can safely save more of them per database operation.
    LOG_BATCH_SIZE = 10000

    # Detection batches are controlled by detection_service.py.
    DETECTION_BATCH_SIZE = 5000

    # Updating the Job row too frequently creates unnecessary
    # database traffic. Update progress every 50,000 parsed logs.
    JOB_UPDATE_INTERVAL = 50000

    def __init__(self):

        self.parser = ApacheLogParser()
        self.threat_detector = ThreatDetector()
        self.brute_force_detector = BruteForceDetector()
        self.aggregation_service = AggregationService()

    def process_file(
        self,
        file_path: Path,
        job_id=None,
    ):

        if job_id is None:
            raise ValueError(
                "job_id is required for processing."
            )

        total_start = perf_counter()

        parsed_count = 0
        detection_count = 0

        log_batch = []
        detection_batch = []

        batch_number = 0

        last_job_update_count = 0

        # =========================================================
        # PROFILING TIMERS
        # =========================================================

        parser_time = 0.0
        threat_detection_time = 0.0
        brute_force_time = 0.0
        aggregation_time = 0.0

        log_db_time = 0.0
        detection_db_time = 0.0
        job_update_time = 0.0

        # =========================================================
        # PROCESS FILE
        # =========================================================

        for raw_log_entry in self.parser.parse_file(file_path):

            # -----------------------------------------------------
            # PARSER / ITERATION
            # -----------------------------------------------------

            start = perf_counter()

            log_entry = raw_log_entry

            parser_time += (
                perf_counter() - start
            )

            parsed_count += 1

            log_batch.append(log_entry)

            # -----------------------------------------------------
            # THREAT DETECTION
            # -----------------------------------------------------

            start = perf_counter()

            threats = self.threat_detector.detect(
                log_entry
            )

            threat_detection_time += (
                perf_counter() - start
            )

            # -----------------------------------------------------
            # PROCESS THREATS
            # -----------------------------------------------------

            for threat in threats:

                threat["job_id"] = job_id

                detection_batch.append(threat)

                start = perf_counter()

                self.aggregation_service.add_detection(
                    threat
                )

                aggregation_time += (
                    perf_counter() - start
                )

            # -----------------------------------------------------
            # BRUTE FORCE DETECTION
            # -----------------------------------------------------

            start = perf_counter()

            brute_force = (
                self.brute_force_detector.process(
                    log_entry
                )
            )

            brute_force_time += (
                perf_counter() - start
            )

            if brute_force:

                brute_force["job_id"] = job_id

                detection_batch.append(
                    brute_force
                )

                start = perf_counter()

                self.aggregation_service.add_detection(
                    brute_force
                )

                aggregation_time += (
                    perf_counter() - start
                )

            # -----------------------------------------------------
            # SAVE LOG BATCH
            # -----------------------------------------------------

            if len(log_batch) >= self.LOG_BATCH_SIZE:

                start = perf_counter()

                save_logs(
                    log_batch,
                    job_id,
                )

                db.session.commit()

                log_db_time += (
                    perf_counter() - start
                )

                log_batch.clear()

                batch_number += 1

                print(
                    f"[PROCESS] Saved log batch "
                    f"{batch_number} | "
                    f"Parsed={parsed_count:,}",
                    flush=True,
                )

            # -----------------------------------------------------
            # SAVE DETECTION BATCH
            # -----------------------------------------------------

            if len(detection_batch) >= self.DETECTION_BATCH_SIZE:

                start = perf_counter()

                save_detections(
                    detection_batch
                )

                db.session.commit()

                detection_db_time += (
                    perf_counter() - start
                )

                detection_count += len(
                    detection_batch
                )

                detection_batch.clear()

                print(
                    f"[PROCESS] Saved detection batch | "
                    f"Total detections="
                    f"{detection_count:,}",
                    flush=True,
                )

            # -----------------------------------------------------
            # JOB PROGRESS UPDATE
            # -----------------------------------------------------
            #
            # IMPORTANT:
            #
            # Previously this happened every 5,000 lines.
            # For ~1 million lines that means ~200 DB updates.
            #
            # Now it happens every 50,000 lines.
            #
            # We intentionally keep the existing 90% ceiling
            # because an exact percentage requires knowing the
            # total number of parser records ahead of time.
            # We will improve this separately after the database
            # performance work is verified.
            # -----------------------------------------------------

            if (
                parsed_count - last_job_update_count
                >= self.JOB_UPDATE_INTERVAL
            ):

                start = perf_counter()

                job = Job.query.get(
                    job_id
                )

                if job:

                    estimated_progress = min(
                        90,
                        10
                        + (
                            parsed_count
                            // self.JOB_UPDATE_INTERVAL
                        )
                        * 4,
                    )

                    job.progress = estimated_progress

                    db.session.commit()

                job_update_time += (
                    perf_counter() - start
                )

                last_job_update_count = (
                    parsed_count
                )

        # =========================================================
        # REMAINING LOGS
        # =========================================================

        if log_batch:

            start = perf_counter()

            save_logs(
                log_batch,
                job_id,
            )

            db.session.commit()

            log_db_time += (
                perf_counter() - start
            )

            print(
                "[PROCESS] Saved final log batch",
                flush=True,
            )

        # =========================================================
        # REMAINING DETECTIONS
        # =========================================================

        if detection_batch:

            start = perf_counter()

            save_detections(
                detection_batch
            )

            db.session.commit()

            detection_db_time += (
                perf_counter() - start
            )

            detection_count += len(
                detection_batch
            )

            print(
                "[PROCESS] Saved final detection batch",
                flush=True,
            )

        # =========================================================
        # FINAL JOB UPDATE
        # =========================================================

        start = perf_counter()

        job = Job.query.get(
            job_id
        )

        if job:

            job.progress = 95

            db.session.commit()

        job_update_time += (
            perf_counter() - start
        )

        # =========================================================
        # FINAL PROFILE
        # =========================================================

        total_time = (
            perf_counter() - total_start
        )

        measured_time = (
            parser_time
            + threat_detection_time
            + brute_force_time
            + aggregation_time
            + log_db_time
            + detection_db_time
            + job_update_time
        )

        unmeasured_time = max(
            0.0,
            total_time - measured_time,
        )

        print(
            "\n"
            "============================================================\n"
            "PROCESSING PROFILE\n"
            "============================================================\n"
            f"Total processing time : "
            f"{total_time:.3f}s\n"
            f"Parsed lines          : "
            f"{parsed_count:,}\n"
            f"Detections            : "
            f"{detection_count:,}\n"
            "\n"
            f"Parser iteration      : "
            f"{parser_time:.3f}s\n"
            f"Threat detection      : "
            f"{threat_detection_time:.3f}s\n"
            f"Brute-force detection : "
            f"{brute_force_time:.3f}s\n"
            f"Aggregation           : "
            f"{aggregation_time:.3f}s\n"
            f"Log database writes   : "
            f"{log_db_time:.3f}s\n"
            f"Detection DB writes   : "
            f"{detection_db_time:.3f}s\n"
            f"Job updates           : "
            f"{job_update_time:.3f}s\n"
            f"Other/unmeasured      : "
            f"{unmeasured_time:.3f}s\n"
            "============================================================\n",
            flush=True,
        )

        print(
            f"[PROCESS COMPLETE] "
            f"Parsed={parsed_count:,} "
            f"Detections={detection_count:,}",
            flush=True,
        )

        return {
            "parsed_count": parsed_count,
            "detection_count": detection_count,
            "summary": (
                self.aggregation_service.get_summary()
            ),
        }