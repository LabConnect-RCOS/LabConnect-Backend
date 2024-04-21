import React from "react";
import FiltersField from "../components/FiltersField";
import PostsField from "./PostsField";
import { useReducer } from "react";
import { useCallback } from "react";
import { useEffect } from "react";

const Posts = () => {
  const reducer = (state, action) => {
    switch (action.type) {
      case "REMOVE_FILTER":
        if (action.filter) {
          state.filters = state.filters.filter((item) => item != action.filter);
        }
        return { ...state };
      case "ADD_FILTER":
        if (action.filter) {
          state.filters.push(action.filter);
        }
        return { ...state };
      case "SET_ACTIVE_ID":
        if (action.id) {
          if (state.jobs.find((job) => job.id === action.id)) {
            state.activeId = action.id;
          }
        }
        return { ...state };
      case "SET_JOBS":
        if (action.jobs) {
          state.jobs = action.jobs;
        }
        return { ...state };
      default:
        return state;
    }
  };

  var [jobState, dispatch] = useReducer(reducer, {
    filters: ["Fall", "Credit", "Remote"],
    activeId: "",
    jobs: [],
  });

  const removeFilter = useCallback((name) => {
    dispatch({ type: "REMOVE_FILTER", filter: name });
  });

  const addFilter = useCallback((name) => {
    dispatch({ type: "ADD_FILTER", filter: name });
  });

  const setActiveId = useCallback((val) => {
    console.log(val);
    dispatch({ type: "SET_ACTIVE_ID", id: val });
  });

  const fetchOpportunities = async () => {
    const url = "http://localhost:8000/getOpportunityCards";

    const response = await fetch(url);

    if (!response.ok) {
      console.log("Error fetching opportunities");
    } else {
      let data = await response.json();
      data = data.data;
      // console.log(data);
      dispatch({ type: "SET_JOBS", jobs: data });
      console.log(jobState.jobs);
    }
  };

  useEffect(() => {
    fetchOpportunities();
  }, [jobState.filters]);

  return (
    <section>
      <FiltersField deleteFilter={removeFilter} filters={jobState.filters} />
      <PostsField
        activeId={jobState.activeId}
        setActive={setActiveId}
        opportunities={jobState.jobs}
      />
    </section>
  );
};

export default Posts;
