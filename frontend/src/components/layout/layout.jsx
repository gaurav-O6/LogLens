import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import "./layout.css";

function Layout({ children }) {
    return (
        <div className="layout">
            <Sidebar />

            <div className="main-content">
                <Topbar />

                <main className="page-content">
                    {children}
                </main>
            </div>
        </div>
    );
}

export default Layout;