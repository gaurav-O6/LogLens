import { useState } from "react";
import { UploadCloud, CheckCircle, AlertCircle } from "lucide-react";
import api from "../api/client";


function UploadBox({ onUpload }) {


    const [file,setFile] = useState(null);

    const [loading,setLoading] = useState(false);

    const [result,setResult] = useState(null);

    const [error,setError] = useState("");



    const handleUpload = async()=>{


        if(!file){

            setError("Please select a .log file");

            return;

        }



        const formData = new FormData();

        formData.append("file",file);



        try{


            setLoading(true);

            setError("");

            setResult(null);



            const response = await api.post(

                "/logs/upload",

                formData,

                {

                    headers:{

                        "Content-Type":
                        "multipart/form-data",

                    },

                }

            );



            setResult(response.data);



            onUpload?.();



        }
        catch(error){


            console.error(error);

            setError(
                "Upload failed. Please try again."
            );


        }
        finally{


            setLoading(false);


        }


    };




    return(


        <div className="upload-box">


            <UploadCloud
                size={48}
            />



            <h2>
                Upload Security Logs
            </h2>



            <p>
                Supports Apache / Nginx .log files
            </p>




            <label className="file-drop">


                <input

                    type="file"

                    accept=".log"

                    onChange={(e)=>
                        setFile(e.target.files[0])
                    }

                />


                <span>

                    {file
                        ? file.name
                        : "Choose log file"
                    }

                </span>


            </label>





            <button

                onClick={handleUpload}

                disabled={loading}

            >

                {
                    loading
                    ?
                    "Analyzing..."
                    :
                    "Upload & Analyze"
                }


            </button>





            {
                result && (

                    <div className="upload-result success">


                        <CheckCircle size={20}/>


                        <div>


                            <strong>
                                Analysis Complete
                            </strong>


                            <p>
                                Parsed Logs:
                                {" "}
                                {result.parsed_logs}
                            </p>


                            <p>
                                Threats:
                                {" "}
                                {result.detections}
                            </p>


                        </div>


                    </div>

                )
            }




            {
                error && (

                    <div className="upload-result error">


                        <AlertCircle size={20}/>


                        <span>
                            {error}
                        </span>


                    </div>

                )
            }



        </div>


    );

}


export default UploadBox;