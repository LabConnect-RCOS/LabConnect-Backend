import React from "react";
import { Modal, Backdrop, Fade } from "@mui/material"; // Import modal components from Material-UI

const FilterModal = ({ open, handleClose }) => {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="transition-modal-title"
      aria-describedby="transition-modal-description"
      BackdropComponent={Backdrop}
      BackdropProps={{
        timeout: 500,
      }}
    >
      <div className="modal">
        <div className="modal-content">
          {/* Modal content (filter options) */}
          <h2 id="transition-modal-title">Filter Options</h2>
          <div id="transition-modal-description">
          <h3>Major</h3>
            <label>
              <input type="checkbox" /> Computer Science
            </label>
            <label>
              <input type="checkbox" /> ITWS
            </label>
            <label>
              <input type="checkbox" /> Mechanical Engineering
            </label>

            <h3>Pay</h3>
            <label>
              <input type="checkbox" /> Paid
            </label>
            <label>
              <input type="checkbox" /> Credit
            </label>
            <label>
              <input type="checkbox" /> Pay + Credit
            </label>

            <h3>Onsite/remote</h3>
            <label>
              <input type="checkbox" /> In person
            </label>
            <label>
              <input type="checkbox" /> Virtual
            </label>

            <h3>Qualifications</h3>
            <label>
              <input type="checkbox" /> Major
            </label>
            <label>
              <input type="checkbox" /> GPA
            </label>
            <label>
              <input type="checkbox" /> School Year
            </label>
            <label>
              <input type="checkbox" /> Graduation Date
            </label>

            <h3>Work Authorization</h3>
            <label>
              <input type="checkbox" /> Jobs that do not require US work authorization
            </label>
            <label>
              <input type="checkbox" /> Jobs that are eligible for US visa sponsorship
            </label>
            <label>
              <input type="checkbox" /> Jobs that are open to candidates with Curricular Practical Training (CPT) and/or Optional Practical Training (OPT)
            </label>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default FilterModal;
