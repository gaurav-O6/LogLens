from pathlib import Path

from app.database.db import db
from app.models.job import Job

from app.parser.apache_parser import ApacheLogParser

from app.detection.detector import ThreatDetector
from app.detection.brute_force import BruteForceDetector

from app.services.aggregation_service import AggregationService
from app.services.log_service import save_logs
from app.services.detection_service import save_detections


class ProcessingService:

    # Larger batches = fewer database round trips
    # while still keeping memory usage reasonable.
    BATCH_SIZE = 5000

    def __init__(self):

        self.parser = ApacheLogParser()

        self.threat_detector = ThreatDetector()

        self.brute_force_detector = BruteForceDetector()

        self.aggregation_service = AggregationService()

    def process_file(
        self,
        file_path: Path,
        job_id=None
    ):

        parsed_count = 0
        detection_count = 0

        log_batch = []
        detection_batch = []

        batch_number = 0

        for log_entry in self.parser.parse_file(file_path):

            parsed_count += 1

            log_batch.append(log_entry)

            threats = self.threat_detector.detect(
                log_entry
            )

            for threat in threats:

                detection_batch.append(threat)

                self.aggregation_service.add_detection(
                    threat
                )

            brute_force = self.brute_force_detector.process(
                log_entry
            )

            if brute_force:

                detection_batch.append(
                    brute_force
                )

                self.aggregation_service.add_detection(
                    brute_force
                )

            #
            # Flush logs every batch
            #
            if len(log_batch) >= self.BATCH_SIZE:

                save_logs(log_batch)

                db.session.commit()

                log_batch.clear()

                batch_number += 1

                if job_id:

                    job = Job.query.get(job_id)

                    if job:

                        #
                        # Progress:
                        # 10 -> 90 during processing
                        #
                        job.progress = min(
                            90,
                            10 + batch_number
                        )

                        db.session.commit()

                print(
                    f"[PROCESS] Saved log batch {batch_number} | Parsed={parsed_count:,}",
                    flush=True
                )

            #
            # Flush detections every batch
            #
            if len(detection_batch) >= self.BATCH_SIZE:

                save_detections(
                    detection_batch
                )

                db.session.commit()

                detection_count += len(
                    detection_batch
                )

                detection_batch.clear()

                print(
                    f"[PROCESS] Saved detection batch | Total detections={detection_count:,}",
                    flush=True
                )

        #
        # Remaining logs
        #
        if log_batch:

            save_logs(log_batch)

            db.session.commit()

            print(
                "[PROCESS] Saved final log batch",
                flush=True
            )

        #
        # Remaining detections
        #
        if detection_batch:

            save_detections(
                detection_batch
            )

            db.session.commit()

            detection_count += len(
                detection_batch
            )

            print(
                "[PROCESS] Saved final detection batch",
                flush=True
            )

        #
        # Ensure final progress
        #
        if job_id:

            job = Job.query.get(job_id)

            if job:

                job.progress = 95

                db.session.commit()

        print(
            f"[PROCESS COMPLETE] Parsed={parsed_count:,}  Detections={detection_count:,}",
            flush=True
        )

        return {

            "parsed_count":
                parsed_count,

            "detection_count":
                detection_count,

            "summary":
                self.aggregation_service.get_summary()

        }