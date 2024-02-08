import React from "react";
import ProfileAvatar from "../components/UIElements/ProfileAvatar";
import EditInformation from "../components/Profile/EditInformation";

const EditProfile = ({id, name, description, email, role, image}) => {
    
    
    
    return <section>
      <div className="flex gap-5">
        <ProfileAvatar name={name} image={image} />
        <EditInformation id={id} name={name} description={description} email={email} role={role} image={image} />
      </div>
      
    </section>
};

export default EditProfile;