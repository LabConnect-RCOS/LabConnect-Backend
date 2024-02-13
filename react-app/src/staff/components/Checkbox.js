import React from "react";

const CheckBox = ({ formHook, errors, errorMessage, name, label, options }) => {
  // if (!formHook) {
  //   return <h1>FormHook Not Given</h1>;
  // }

  return (
    <div>
      <div className=" w-full max-w-xs">
        <div className="label">
          <span className="label-text font-medium">{label}</span>
        </div>
        {errors && errors[name] && (
          <p className="text-red-500">{errorMessage}</p>
        )}

        <div className="flex flex-col gap-2">
          {options &&
            options.map((item) => {
              return (
                <div key={item} className="form-control">
                  <label className="cursor-pointer label">
                    <span className="label-text">{item}</span>
                    <input
                      type="checkbox"
                      value={item}
                      {...formHook}
                      id={item}
                      className="checkbox"
                    />
                  </label>
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
};

export default CheckBox;
