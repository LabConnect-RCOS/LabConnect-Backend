import React from "react";
import { Modal, Backdrop, Fade, Typography, Checkbox, FormControlLabel, Select, MenuItem } from "@mui/material";

const FilterModal = ({ open, handleClose }) => {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="transition-modal-title"
      aria-describedby="transition-modal-description"
      closeAfterTransition
      BackdropComponent={Backdrop}
      BackdropProps={{
        timeout: 500,
      }}
    >
      <Fade in={open}>
        <div style={{
          backgroundColor: 'white',
          padding: 20,
          width: 400,
          maxWidth: '90%',
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          outline: 'none',
          borderRadius: 8,
        }}>
          <Typography variant="h5" gutterBottom>
            Filter Options
          </Typography>
          <div>
            <Typography variant="h6" gutterBottom>
              Major
            </Typography>
            <FormControlLabel
              control={<Checkbox />}
              label="Computer Science"
            />
            <FormControlLabel
              control={<Checkbox />}
              label="ITWS"
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Mechanical Engineering"
            />
          </div>
          <div>
            <Typography variant="h6" gutterBottom>
              Pay
            </Typography>
            <FormControlLabel
              control={<Checkbox />}
              label="Paid"
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Credit"
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Pay + Credit"
            />
          </div>
          <div>
            <Typography variant="h6" gutterBottom>
              Onsite/Remote
            </Typography>
            <FormControlLabel
              control={<Checkbox />}
              label="In person"
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Virtual"
            />
          </div>
          <div>
            <Typography variant="h6" gutterBottom>
              Department
            </Typography>
            <Select>
              <MenuItem value="engineering">School of Engineering</MenuItem>
              <MenuItem value="science">School of Science</MenuItem>
              <MenuItem value="business">Lally School of Management</MenuItem>
              {/* Add more department options as needed */}
            </Select>
          </div>
          <div>
            <Typography variant="h6" gutterBottom>
              Salary Range
            </Typography>
            <Select>
              <MenuItem value="<15">&lt; $15</MenuItem>
              <MenuItem value="15-18">$15 - $18</MenuItem>
              <MenuItem value="18">$18</MenuItem>
            </Select>
          </div>
        </div>
      </Fade>
    </Modal>
  );
};

export default FilterModal;
