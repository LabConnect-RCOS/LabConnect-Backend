import React, { useState } from "react";
import { Modal, Fade, Typography, Checkbox, FormControlLabel, Select, MenuItem, Button } from "@mui/material";

const FormHeader = ({ handleClose }) => {
  return (
    <div style={{ backgroundColor: 'white', position: 'sticky', top: 0, zIndex: 1, height: 80, padding: '25px 20px', borderBottom: '1px solid #ccc' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
        <Typography variant="h5" gutterBottom style={{ fontWeight: 'bold' }}>
          Filter Options
        </Typography>
        <Button onClick={handleClose} style={{ fontWeight: 'bold' }}>X</Button>
      </div>
    </div>
  );
};

const FormFooter = ({ handleClear, handleShowResults }) => {
  return (
    <div style={{ backgroundColor: 'white', borderTop: '1px solid #ccc', padding: '10px 20px', boxShadow: '0px 3px 5px -1px rgba(0,0,0,0.2), 0px 6px 10px 0px rgba(0,0,0,0.14), 0px 1px 18px 0px rgba(0,0,0,0.12)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button onClick={handleClear} variant="outlined" color="error">Clear</Button>
        <Button onClick={handleShowResults} variant="contained" color="primary">Show Results</Button>
      </div>
    </div>
  );
};

const FormContent = ({ checkedItems, setCheckedItems, selectedDepartment, setSelectedDepartment, selectedSalaryRange, setSelectedSalaryRange }) => {
  return (
    <div style={{ overflowY: 'auto', maxHeight: 'calc(80vh - 172px)', padding: '20px', paddingRight: '20px' }}>
      <div>
        <Typography variant="h6" gutterBottom>
          Major
        </Typography>
        <FormControlLabel
          control={<Checkbox checked={checkedItems.computerScience} onChange={() => setCheckedItems({ ...checkedItems, computerScience: !checkedItems.computerScience })} />}
          label="Computer Science"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.itws} onChange={() => setCheckedItems({ ...checkedItems, itws: !checkedItems.itws })} />}
          label="ITWS"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.mechanicalEngineering} onChange={() => setCheckedItems({ ...checkedItems, mechanicalEngineering: !checkedItems.mechanicalEngineering })} />}
          label="Mechanical Engineering"
        />
      </div>
      <div>
        <Typography variant="h6" gutterBottom>
          Pay
        </Typography>
        <FormControlLabel
          control={<Checkbox checked={checkedItems.paid} onChange={() => setCheckedItems({ ...checkedItems, paid: !checkedItems.paid })} />}
          label="Paid"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.credit} onChange={() => setCheckedItems({ ...checkedItems, credit: !checkedItems.credit })} />}
          label="Credit"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.payCredit} onChange={() => setCheckedItems({ ...checkedItems, payCredit: !checkedItems.payCredit })} />}
          label="Pay + Credit"
        />
      </div>
      <div>
        <Typography variant="h6" gutterBottom>
          Onsite/Remote
        </Typography>
        <FormControlLabel
          control={<Checkbox checked={checkedItems.onsite} onChange={() => setCheckedItems({ ...checkedItems, onsite: !checkedItems.onsite })} />}
          label="Onsite"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.remote} onChange={() => setCheckedItems({ ...checkedItems, remote: !checkedItems.remote })} />}
          label="Remote"
        />
        <FormControlLabel
          control={<Checkbox checked={checkedItems.hybrid} onChange={() => setCheckedItems({ ...checkedItems, hybrid: !checkedItems.hybrid })} />}
          label="Hybrid"
        />
      </div>
      <div>
        <Typography variant="h6" gutterBottom>
          Department
        </Typography>
        <Select value={selectedDepartment} onChange={(event) => setSelectedDepartment(event.target.value)}>
          <MenuItem value="engineering">School of Engineering</MenuItem>
          <MenuItem value="science">School of Science</MenuItem>
          <MenuItem value="business">Lally School of Management</MenuItem>
        </Select>
      </div>
      <div>
        <Typography variant="h6" gutterBottom>
          Salary Range
        </Typography>
        <Select value={selectedSalaryRange} onChange={(event) => setSelectedSalaryRange(event.target.value)}>
          <MenuItem value="<15">&lt; $15</MenuItem>
          <MenuItem value="15-18">$15 - $18</MenuItem>
          <MenuItem value="18">$18</MenuItem>
        </Select>
      </div>
    </div>
  );
};

const FilterModal = ({ open, handleClose }) => {
  const [checkedItems, setCheckedItems] = useState({
    computerScience: false,
    itws: false,
    mechanicalEngineering: false,
    paid: false,
    credit: false,
    payCredit: false,
    onsite: false,
    remote: false,
    hybrid: false,
  });

  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [selectedSalaryRange, setSelectedSalaryRange] = useState('');

  const handleClear = () => {
    setCheckedItems({
      computerScience: false,
      itws: false,
      mechanicalEngineering: false,
      paid: false,
      credit: false,
      payCredit: false,
      onsite: false,
      remote: false,
      hybrid: false,
    });

    setSelectedDepartment('');
    setSelectedSalaryRange('');
  };

  const handleShowResults = () => {
    // need to add code to show results here
  };

  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="transition-modal-title"
      aria-describedby="transition-modal-description"
      closeAfterTransition
    >
      <Fade in={open}>
        <div style={{
          backgroundColor: 'white',
          width: 400,
          maxWidth: '100%',
          maxHeight: '80%',
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          outline: 'none',
          borderRadius: 8,
          display: 'flex',
          flexDirection: 'column',
        }}>
          <FormHeader handleClose={handleClose} />
          <FormContent
            checkedItems={checkedItems}
            setCheckedItems={setCheckedItems}
            selectedDepartment={selectedDepartment}
            setSelectedDepartment={setSelectedDepartment}
            selectedSalaryRange={selectedSalaryRange}
            setSelectedSalaryRange={setSelectedSalaryRange}
          />
          <div style={{ flex: 1 }}></div>
          <FormFooter handleClear={handleClear} handleShowResults={handleShowResults} />
        </div>
      </Fade>
    </Modal>
  );
};

export default FilterModal;
