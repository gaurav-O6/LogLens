import {
    Shield,
    LayoutDashboard,
    UploadCloud,
    AlertTriangle,
    BarChart3,
    History,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import "./sidebar.css";


const menuItems = [
    {
        name: "Overview",
        icon: LayoutDashboard,
        path: "/"
    },
    {
        name: "Upload Logs",
        icon: UploadCloud,
        path: "/upload"
    },
    {
        name: "Threats",
        icon: AlertTriangle,
        path: "/threats"
    },
    {
        name: "Analytics",
        icon: BarChart3,
        path: "/analytics"
    },
    {
        name: "History",
        icon: History,
        path: "/history"
    }
];


function Sidebar() {

    const navigate = useNavigate();


    return (

        <aside className="sidebar">


            <div className="sidebar-header">

                <div className="logo-icon">
                    <Shield size={22} />
                </div>


                <div>
                    <h2>LogLens</h2>

                    <span>
                        Security Operations
                    </span>
                </div>

            </div>



            <nav className="sidebar-nav">

                {
                    menuItems.map((item) => {

                        const Icon = item.icon;


                        return (

                            <div
                                key={item.name}
                                className="nav-item"
                                onClick={() => navigate(item.path)}
                            >

                                <Icon size={18} />

                                <span>
                                    {item.name}
                                </span>

                            </div>

                        );

                    })
                }

            </nav>



            <div className="sidebar-footer">

                SYSTEM v1.0.0

            </div>


        </aside>

    );

}


export default Sidebar;