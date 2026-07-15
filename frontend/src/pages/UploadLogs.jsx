import UploadBox from "../components/UploadBox";
import "./Page.css";


function UploadLogs(){


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



            <UploadBox />


        </div>


    );

}


export default UploadLogs;