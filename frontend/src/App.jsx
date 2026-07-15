import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";


import Layout from "./components/layout/Layout";


import Dashboard from "./pages/Dashboard";
import UploadLogs from "./pages/UploadLogs";
import Threats from "./pages/Threats";
import Analytics from "./pages/Analytics";
import History from "./pages/History";
import Settings from "./pages/Settings";



function App(){


    return (

        <BrowserRouter>

            <Layout>

                <Routes>


                    <Route
                        path="/"
                        element={<Dashboard />}
                    />


                    <Route
                        path="/upload"
                        element={<UploadLogs />}
                    />


                    <Route
                        path="/threats"
                        element={<Threats />}
                    />


                    <Route
                        path="/analytics"
                        element={<Analytics />}
                    />


                    <Route
                        path="/history"
                        element={<History />}
                    />


                    <Route
                        path="/settings"
                        element={<Settings />}
                    />


                </Routes>

            </Layout>

        </BrowserRouter>

    );

}


export default App;