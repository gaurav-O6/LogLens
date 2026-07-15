import "./Page.css";


function History(){

    return (

        <div className="page">


            <div className="page-heading">

                <h1>
                    Analysis History
                </h1>


                <p>
                    Previous log analysis sessions will appear here
                </p>


            </div>


            <div className="empty-state">

                No analysis history available yet

            </div>


        </div>

    );

}


export default History;