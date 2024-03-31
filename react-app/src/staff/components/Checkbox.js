import React from "react";

const CheckBox = ({ formHook, errors, errorMessage, name, label, options, type }) => {
  // if (!formHook) {
  //   return <h1>FormHook Not Given</h1>;
  // }

  return (
    <div>
      <div className="check-input">
        <div className="label">
          <span className="label-text font-medium">{label}</span>
        </div>
        {errors && errors[name] && (
          <p className="text-red-500">{errorMessage}</p>
        )}

        <div className="flex2 gap-2">
          {options &&
            options.map((item) => {
              return (
                <div key={item} className="form-control">
                  <label className="cursor-pointer label">
                    <span className="label-text">{item}</span>
                    <input
                      type={type == "radio" ? "radio" : "checkbox"}
                      value={item}
                      {...formHook}
                      id={item}
                      className={type == "radio" ? "radio" : "checkbox"}
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
