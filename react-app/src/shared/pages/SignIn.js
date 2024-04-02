import React, { useEffect } from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import useGlobalContext from "../../context/global/useGlobalContext";

import Input from "../../staff/components/Input.js"

const SignIn = () => {

    const [loading, setLoading] = useState(false);

    const submitHandler = (data) => {
        if (authorId) {
          console.log({...data, authorId});
        }
      };
      const state = useGlobalContext();
      const { loggedIn } = state;
      const { id: authorId } = state;

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
        <form
          onSubmit={handleSubmit((data) => {
            submitHandler(data);
          })}
          className="flex2 gap-2"
        >
    
        <Input
            label="RCS ID"
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
            label="password"
            name={"password"}
            errors={errors}
            errorMessage={"Passowrd must be between 8 and 30 characters"}
            formHook={{
              ...register("password", {
                required: true,
                minLength: 8,
                maxLength: 30,
              }),
            }}
          />
          
    
    
          <input type="submit" className="btn btn-primary bg-blue-700" />
        </form>
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
