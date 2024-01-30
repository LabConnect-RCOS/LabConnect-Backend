import React from "react";

const Input = ({ type, name, formHook, label, options, placeHolder }) => {
  // if (!formHook) {
  //   return <h1>FormHook Not Given</h1>;
  // }

  const inputElement = (
    <input
      {...formHook}
      type={type || "text"}
      list={options && name}
      placeholder={placeHolder || "Type Here"}
      className="input input-bordered w-full max-w-xs"
    />
  );
  
  

  const textAreaElement = (
    <textarea
    
      {...formHook}
      placeholder={placeHolder || "Type Here"}
      cols="50"
      rows="10"
      className="border-2 rounded p-2 m-0"
    ></textarea>
  );

  return (
    <div>
      <label className=" w-full max-w-xs">
        <div className="label">
          <span className="label-text font-medium">{label}</span>
        </div>
        {((type != "textarea" || !type) && inputElement)}
        {(type == "textarea" && textAreaElement)}
        
      </label>
    </div>
  );
};

export default Input;
