import React, { useEffect } from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import Input from "../../staff/components/Input.js"
import StickyFooter from "../components/Navigation/StickyFooter.js"

import logo from "../../images/LabConnect_Logo2.png";
console.log(logo);

const SignIn = () => {
    const [loading, setLoading] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
        reset
      } = useForm({
        defaultValues: {
          rcsid: "",
          password: "",
        },
      });

    var forms = (
      <section className="flex2 h-screen justify-between">
        <section className="flex2 justify-center text-center">
          <br />
          <div className="flex justify-center items-center">
            <img src={logo} alt="Logo" />
          </div>
          <br />
          <form
            onSubmit={handleSubmit((data) => {
              console.log(...data);
            })}
            className="gap-2 px-96"
          >
      
          <Input
              label="Username / RCS ID"
              name={"rcsid"}
              errors={errors}
              errorMessage={"RCSID must be between 2 and 9 characters"}
              formHook={{
                ...register("rcsid", {
                  required: true,
                  minLength: 2,
                  maxLength: 9,
                }),
              }}
          />

          <Input
              label="Password"
              name={"password"}
              errors={errors}
              errorMessage={"Password must be between 8 and 30 characters"}
              formHook={{
                ...register("password", {
                  required: true,
                  minLength: 8,
                  maxLength: 30,
                }),
              }}
            />
            
            <br/><br/>
      
            <input type="submit" value="Log In" className="btn btn-primary w-full"/>
          </form>
        </section>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <StickyFooter/>
      </section>
    );
  
    return !loading ? (
      forms
    ) : loading === "no response" ? (
      <h1>There was no response</h1>
    ) : (
      <span className="creationforms-loading" />
    );
};

export default SignIn;
