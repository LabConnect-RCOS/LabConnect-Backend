import React from "react";

const JobDescription = ({ description }) => {
  return (
    <article className='flex flex-col gap-2'>
      <div className='font-extrabold text-xl'>Role Description</div>

      <div className='text-gray-700'>{description}</div>
    </article>
  );
};

export default JobDescription;
