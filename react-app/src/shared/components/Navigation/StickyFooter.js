import { Link } from "react-router-dom";
import logo from "../../../images/LabConnect_Logo.png"; 
console.log(logo);

const StickyFooter = () => {
    return (
        <section className="stickyfooter-general">
            <p className="stickyfooter-header">
                Made by <Link to="https://new.rcos.io" className="no-underline text-red-400">RCOS</Link>
            </p>
            <div className="stickyfooter-info">
                <div className="pb-3">
                    <img src={logo} alt="Logo" className="h-32 w-36"></img>
                </div>

                <div className="w-40">
                    <p>
                        <b>Contact Us</b>
                        <p className="text-base">
                            <Link to="https://github.com/LabConnect-RCOS" className="stickyfooter-link hover:text-neutral-950">Discord</Link><br/>
                            <Link to="https://discord.gg/STtGsX86" className="stickyfooter-link hover:text-neutral-950">GitHub</Link><br/>
                        </p>
                    </p>
                </div>
                <div className="w-40 text-base">
                    <b>Student Pages</b>
                    <p>
                        <Link to="/jobs" className="stickyfooter-link hover:text-neutral-950">Jobs</Link><br/>
                        <Link to="/staff" className="stickyfooter-link hover:text-neutral-950">Staff</Link><br/>
                        <Link to="/signIn" className="stickyfooter-link hover:text-neutral-950">Sign In</Link><br/>
                    </p>
                </div>
                <div className="w-60 text-base">
                    <b>Staff Pages</b>
                    <p>
                        <Link to="/profile" className="stickyfooter-link hover:text-neutral-950">Profile</Link><br/>
                        <Link to="/createPost" className="stickyfooter-link hover:text-neutral-950">Create</Link><br/>
                        <Link to="/jobs" className="stickyfooter-link hover:text-neutral-950">Jobs</Link><br/>
                        <Link to="/signIn" className="stickyfooter-link hover:text-neutral-950">Sign In</Link><br/>
                    </p>
                </div>
            </div>
        </section>
    )
};

export default StickyFooter;
