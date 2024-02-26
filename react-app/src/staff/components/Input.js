import React from "react";

const Input = ({
  type,
  errorMessage,
  errors,
  name,
  formHook,
  label,
  options,
  placeHolder,
}) => {
  // if (!formHook) {
  //   return <h1>FormHook Not Given</h1>;
  // }

  const inputElement = (
    <input
      {...formHook}
      type={type || "text"}
      list={options && name}
      placeholder={placeHolder || "Type Here"}
      className="input input-bordered w-full"
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

  const selectElement = (
    <select
      {...formHook}
      defaultValue="Select a department"
      className="select select-bordered w-full max-w-xs"
    >
      <option value="Select a department">
        Select a department
      </option>
      {options ? (
        options.map((option) => {
          return (
            <option key={option} value={option}>
              {option}
            </option>
          );
        })
      ) : (
        <option value="default">Any</option>
      )}
    </select>
  );

  return (
    <div>
      <label className=" w-full max-w-xs">
        <div className="label">
          <span className="label-text font-medium">{label}</span>
        </div>
        {type == "select"
          ? selectElement
          : type == "textarea"
          ? textAreaElement
          : inputElement}

        {errors && errors[name] && (
          <p className="text-red-500">{errorMessage}</p>
        )}
      </label>
    </div>
  );
};

export default Input;
