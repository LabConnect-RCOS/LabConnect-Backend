import React from "react";

const CheckBox = ({ formHook, label, options }) => {
  // if (!formHook) {
  //   return <h1>FormHook Not Given</h1>;
  // }

  return (
    <div>
      <label className=" w-full max-w-xs">
        <div className="label">
          <span className="label-text font-medium">{label}</span>
        </div>

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
      </label>
    </div>
  );
};

export default CheckBox;
