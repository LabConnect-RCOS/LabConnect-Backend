import React from "react";
import { useForm } from "react-hook-form";
import CheckBox from "./Checkbox";
import Input from "./Input";

const CreationForms = () => {
  const {
    register,
    handleSubmit,
    // formState: { errors },
  } = useForm();

  const submitHandler = (data) => {
    console.log(data);
  };

  return (
    <form
      onSubmit={handleSubmit((data) => {
        submitHandler(data);
      })}
      className="flex flex-col gap-2"
    >
      {/* <select {...register("department")} name="myList" id="" className="border">
        <option className="text-black" value="Computer Science">CS</option>
        <option value="Biology">Bio</option>
        <option value="Physics">Phys</option>
      </select> */}

      <Input
        label="Title"
        formHook={{
          ...register("title", {
            required: true,
            minLength: 5,
            maxLength: 100,
          }),
        }}
      />



      <Input
        label="Department"
        formHook={{
          ...register("department", {
            required: true,
            minLength: 3,
            maxLength: 40,
          }),
        }}
      />
      <Input
        label="Location"
        formHook={{
          ...register("location", {
            required: true,
            minLength: 5,
            maxLength: 100,
          }),
        }}
      />
      <Input label="Due Date" formHook={{ ...register("date") }} type="date" />
      <Input
        label="Upfront Pay"
        formHook={{
          ...register("upfrontPay", {
            required: true,
            min: 0,
          }),
        }}
        type="number"
      />
      <Input
        label="Salary"
        formHook={{
          ...register("salary", {
            required: true,
            min: 0,
          }),
        }}
        type="number"
      />
      <Input
        label="Credits"
        formHook={{
          ...register("credits", {
            required: true,
            min: 0,
            max: 4,
          }),
        }}
        type="number"
      />
      <Input
        label="Description"
        formHook={{
          ...register("description", {
            required: true,
            minLength: 10,
          }),
        }}
        type="textarea"
      />

      <CheckBox
        label="Eligible Class Years"
        options={["Freshman", "Sophomore", "Junior", "Senior"]}
        formHook={{ ...register("years") }}
      />

      <input type="submit" className="bg-blue-700" />
    </form>
  );
};

export default CreationForms;
