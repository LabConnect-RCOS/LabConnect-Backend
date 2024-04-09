import { Link } from "react-router-dom";
import logo from "../../../images/LabConnect_Logo.png"; 
console.log(logo);

const StickyFooter = () => {
    return (
        <section className="border-2 rounded p-3">
            <p className="text-center text-lg justify-center">
            Made by <Link to="https://new.rcos.io" className="no-underline text-red-400">RCOS</Link>
            </p>
            <div className="flex flex-row justify-between px-12">
                <div className="pb-3">
                    <img src={logo} alt="Logo" className="h-32 w-36"></img>
                </div>

                <div className="w-40">
                    <p>
                        <b>Contact Us</b>
                        <p className="text-base">
                            dummyemail@gmail.com<br/>other info(github/disc)
                        </p>
                    </p>
                </div>
                <div className="w-40 text-base">
                    <b>Student Pages</b>
                    <p>
                        <Link to="/jobs" className="no-underline text-neutral-600 hover:text-neutral-950">Jobs</Link><br/>
                        <Link to="/staff" className="no-underline text-neutral-600 hover:text-neutral-950">Staff</Link><br/>
                        <Link to="/" className="no-underline text-neutral-600 hover:text-neutral-950">Sign In</Link><br/>
                    </p>
                </div>
                <div className="w-60 text-base">
                    <b>Staff Pages</b>
                    <p>
                        <Link to="/profile" className="no-underline text-neutral-600 hover:text-neutral-950">Profile</Link><br/>
                        <Link to="/createPost" className="no-underline text-neutral-600 hover:text-neutral-950">Create</Link><br/>
                        <Link to="/jobs" className="no-underline text-neutral-600 hover:text-neutral-950">Jobs</Link><br/>
                        <Link to="/" className="no-underline text-neutral-600 hover:text-neutral-950">Sign In</Link><br/>
                    </p>
                </div>
            </div>
        </section>
    )
};

export default StickyFooter;
