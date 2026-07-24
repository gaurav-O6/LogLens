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


            log_batch.append(
                log_entry
            )



            threats = self.threat_detector.detect(
                log_entry
            )



            for threat in threats:


                detection_batch.append(
                    threat
                )


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




            if len(log_batch) >= self.BATCH_SIZE:


                save_logs(
                    log_batch
                )


                log_batch.clear()


                batch_number += 1



                if job_id:


                    job = Job.query.get(
                        job_id
                    )


                    if job:


                        job.progress = min(
                            90,
                            10 + batch_number
                        )


                        db.session.commit()



                print(
                    f"[PROCESS] batch={batch_number} parsed={parsed_count}",
                    flush=True
                )





            if len(detection_batch) >= self.BATCH_SIZE:


                save_detections(
                    detection_batch
                )


                detection_count += len(
                    detection_batch
                )


                detection_batch.clear()





        if log_batch:

            save_logs(
                log_batch
            )



        if detection_batch:

            save_detections(
                detection_batch
            )

            detection_count += len(
                detection_batch
            )



        print(
            f"[PROCESS COMPLETE] parsed={parsed_count} detections={detection_count}",
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