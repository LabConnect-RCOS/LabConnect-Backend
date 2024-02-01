import React from "react";
import { useForm } from "react-hook-form";
import CheckBox from "./Checkbox";
import Input from "./Input";

const CreationForms = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
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
        name={"title"}
        errors={errors}
        errorMessage={"Title must be at least 5 characters"}
        formHook={{
          ...register("title", {
            required: true,
            minLength: 5,
            maxLength: 100,
            
          }),
        }}
      />

      {errors.title && console.log(errors.title.message)}

      <Input
        errors={errors}
        label="Department"
        name={"department"}
        errorMessage={"Department must be at least 3 characters"}
        formHook={{
          ...register("department", {
            required: true,
            minLength: 3,
            maxLength: 40,
            
          }),
        }}
      />
      <Input
        errors={errors}
        label="Location"
        name={"location"}
        errorMessage={"Location must be at least 5 characters"}
        formHook={{
          ...register("location", {
            required: true,
            minLength: 5,
            maxLength: 100,
            
          }),
        }}
      />
      <Input
        errors={errors}
        label="Due Date"
        name={"date"}
        errorMessage={"Due Date is required"}
        formHook={{ ...register("date", {required:true}) }}
        type="date"
      />
      <Input
        errors={errors}
        label="Upfront Pay"
        name={"upfrontPay"}
        errorMessage={"Upfront Pay must be at least 0"}
        formHook={{
          ...register("upfrontPay", {
            required: true,
            min: 0,
            
          }),
        }}
        type="number"
      />
      <Input
        errors={errors}
        label="Salary"
        name={"salary"}
        errorMessage={"Salary must be at least 0"}
        formHook={{
          ...register("salary", {
            required: true,
            min: 0,
            
          }),
        }}
        type="number"
      />
      <Input
        errors={errors}
        label="Credits"
        name={"credits"}
        errorMessage={"Credits must be between 0 and 4"}
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
        errors={errors}
        label="Description"
        name={"description"}
        errorMessage="Description must be at least 10 characters"
        formHook={{
          ...register("description", {
            required: true,
            minLength: 10,
            message: "Description must be at least 10 characters",
          }),
        }}
        type="textarea"
      />

      <CheckBox
        label="Eligible Class Years"
        options={["Freshman", "Sophomore", "Junior", "Senior"]}
        errors={errors}
        errorMessage={"At least one year must be selected"}
        name={"years"}
        formHook={{ ...register("years", {required:true}) }}
      />

      <input type="submit" className="btn btn-primary bg-blue-700" />
    </form>
  );
};

export default CreationForms;
