import React from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useEffect } from "react";
import CheckBox from "./Checkbox";
import Input from "./Input";
import { useParams } from "react-router";
import useGlobalContext from "../../context/global/useGlobalContext";

const DUMMY_DATA = {
  d1: {
    id: "d1",
    title: "Software Intern",
    department: "Computer Science",
    location: "Remote",
    application_due: "2024-02-08",
    upfrontPay: 0,
    salary: 0,
    credits: 0,
    description: "This is a software internship",
    years: ["Freshman", "Junior", "Senior"],
  },
};

const CreationForms = () => {
  const { postID } = useParams();
  const [loading, setLoading] = useState(false);
  const state = useGlobalContext();
  const { loggedIn } = state;
  const { id: authorId } = state;

  async function fetchDetails(key) {
    const url = "http://localhost:8000/getOpportunityMeta/" + key;

    const response = await fetch(url);
    if (!response.ok) {
      return false;
    } else {
      const data = await response.json();
      return data.data;
    }
  }

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    getValues,
  } = useForm({
    defaultValues: {
      id: "",
      name: "",
      //department: "",
      location: "",
      application_due: "",
      active: true,
      credits: [],
      description: "",
      recommended_experience: "",
      semester: [],
      pay: 0,
      years: [],
      year: 2024,
    },
  });

  async function fetchData(key) {
    const response = await fetchDetails(key);
    response && reset(response);

    response ? setLoading(false) : setLoading("no response");
    console.log(getValues());
  }

  useEffect(() => {
    postID && setLoading(true);
    postID && fetchData(postID);
  }, []);

  const createOpportunity = async (data) => {
    const url = "http://localhost:8000/createOpportunity";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      console.log("Failed to create opportunity");
    } else {
      console.log("Opportunity created");

      // redirect to the profile page
      window.location.href = "/profile";
    }
  };

  const updateOpportunity = async (data) => {
    const url = "http://localhost:8000/editOpportunity";

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      console.log("Failed to edit opportunity");
    } else {
      console.log("Opportunity edited");

      // redirect to the profile page
      window.location.href = "/profile";
    }
  };

  const submitHandler = (data) => {
    // convert pay and credits to numbers
    const { id } = state;

    data.pay = +data.pay;

    data.active = true;

    console.log({ ...data, authorID: id });

    // send data to the backend
    !postID && createOpportunity({ ...data, authorID: id });
    postID && updateOpportunity({ ...data, authorID: id });
  };

  var forms = (
    <form
      onSubmit={handleSubmit((data) => {
        submitHandler(data);
      })}
      className="flex2 gap-2"
    >
      {/* <select {...register("department")} name="myList" id="" className="border">
        <option className="text-black" value="Computer Science">CS</option>
        <option value="Biology">Bio</option>
        <option value="Physics">Phys</option>
      </select> */}

      <Input
        label="Title"
        name={"name"}
        errors={errors}
        errorMessage={"Title must be at least 5 characters"}
        formHook={{
          ...register("name", {
            required: true,
            minLength: 5,
            maxLength: 100,
          }),
        }}
      />

      <Input
        errors={errors}
        label="Location"
        name={"location"}
        type="select"
        options={[
          "Amos Eaton",
          "Carnegie",
          "Center for Computational Innovations",
          "Center for Biotechnology and Interdisciplinary Studies",
          "Cogswell Laboratory",
          "Darrin Communications Center",
          "Experimental Media and Performing Arts Center",
          "Greene Library",
          "Jonsson Engineering Center",
          "Lally Hall",
          "Low Center for Industrial Innovation (CII)",
          "LINAC Facility (Gaerttner Laboratory)",
          "Materials Research Center",
          "Pittsburgh Building",
          "Ricketts Building",
          "Russell Sage Laboratory",
          "Jonsson-Rowland Science Center",
          "Voorhees Computing Center",
          "Walker Laboratory",
          "West Hall",
          "Winslow Building",
          "Remote",
          "TBD",
        ]}
        errorMessage={"Location must be selected"}
        formHook={{
          ...register("location", {
            required: true,
            minLength: 3,
            maxLength: 40,
          }),
        }}
      />

      <Input
        errors={errors}
        label="Due Date"
        name={"application_due"}
        errorMessage={"Due Date is required"}
        formHook={{ ...register("application_due", { required: true }) }}
        type="date"
      />

      <Input
        errors={errors}
        label="Pay"
        name={"pay"}
        errorMessage={"Pay must be at least 0"}
        formHook={{
          ...register("pay", {
            required: true,
            min: 0,
          }),
        }}
        type="number"
      />

      <CheckBox
        label="Credit Options"
        options={["1", "2", "3", "4"]}
        errors={errors}
        errorMessage={""}
        name={"years"}
        formHook={{ ...register("credits", { required: false }) }}
      />

      {/* <Input
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
      /> */}

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

      <Input
        errors={errors}
        label="Recommended Experience"
        name={"recommended_experience"}
        errorMessage="Recommended experience must be at least 10 characters"
        formHook={{
          ...register("recommended_experience", {
            required: true,
            minLength: 10,
            message: "Recommended experience must be at least 10 characters",
          }),
        }}
        type="textarea"
      />

      <CheckBox
        label="Eligible Semesters"
        options={["FALL", "SPRING", "SUMMER"]}
        errors={errors}
        errorMessage={"At least one semester must be selected"}
        name={"semester"}
        formHook={{ ...register("semester", { required: true }) }}
        type="radio"
      />

      <CheckBox
        label="Required Courses"
        options={["CSCI4430", "CSCI2961", "CSCI4390"]}
        errors={errors}
        errorMessage={"At least one course must be selected"}
        name={"courses"}
        formHook={{ ...register("courses", { required: true }) }}
      />

      <CheckBox
        label="Eligible Majors"
        options={["CSCI", "PHYS", "BIOL"]}
        errors={errors}
        errorMessage={"At least one major must be selected"}
        name={"majors"}
        formHook={{ ...register("majors", { required: true }) }}
      />

      <CheckBox
        label="Eligible Years"
        options={["2022", "2023", "2024"]}
        errors={errors}
        errorMessage={"At least one year must be selected"}
        name={"years"}
        formHook={{ ...register("years", { required: true }) }}
      />
      <section className="pt-3 pb-5">
        <input type="submit" className="btn btn-primary bg-blue-700 w-full" />
      </section>
    </form>
  );

  return !loading ? (
    forms
  ) : loading === "no response" ? (
    <h1>There was no response</h1>
  ) : (
    <span className="lc-loading" />
  );
};

export default CreationForms;
