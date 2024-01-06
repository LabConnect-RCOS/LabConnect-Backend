import React from "react";

const AboutSectionElement = ({title, description}) => {
    return <div className="flex flex-col gap-1">
        <h5 className="text-gray-500 text-base">{title}</h5>
        <h6 className="font-extrabold">{description}</h6>
    </div>
}

export default AboutSectionElement;