import { useNavigate } from "react-router-dom";

import UploadBox from "../components/UploadBox";

import "./Page.css";



function UploadLogs(){


    const navigate = useNavigate();




    return(

        <div className="page">


            <div className="page-heading">


                <h1>
                    Upload Logs
                </h1>



                <p>
                    Analyze Apache and Nginx security logs
                </p>


            </div>





            <UploadBox

                onComplete={() =>
                    navigate("/")
                }

            />



        </div>

    );

}


export default UploadLogs;