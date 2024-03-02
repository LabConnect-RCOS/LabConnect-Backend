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
            
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default FilterModal;
