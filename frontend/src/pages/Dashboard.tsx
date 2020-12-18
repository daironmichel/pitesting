import React from "react";
import axios from "axios";
import debounce from "lodash.debounce";
import Button from "../components/Button";
import FormInput from "../components/FormInput";

function Dashboard() {
  const [speed, setSpeed] = React.useState("100");
  const [frequency, setFrequency] = React.useState("3000");
  const [transition, setTransition] = React.useState("1");

  const axiosInstance = axios.create({ baseURL: window.location.origin });
  const raiseDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/up", {
        speed,
        frequency,
        transition,
      });
    } catch (e) {
      console.error(e);
    }
  };

  const lowerDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/down", {
        speed,
        frequency,
        transition,
      });
    } catch (e) {
      console.error(e);
    }
  };

  const stopDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/stop", {
        speed,
        frequency,
        transition,
      });
    } catch (e) {
      console.error(e);
    }
  };

  const submitSpeed = debounce(async (speed: string) => {
    try {
      await axiosInstance.post("/api/desk/motor", { speed });
    } catch (e) {
      console.error(e);
    }
  }, 500);

  const submitFrequency = debounce(async (frequency: string) => {
    try {
      await axiosInstance.post("/api/desk/motor", { frequency });
    } catch (e) {
      console.error(e);
    }
  }, 500);

  const submitTransition = debounce(async (transition: string) => {
    try {
      await axiosInstance.post("/api/desk/motor", { transition });
    } catch (e) {
      console.error(e);
    }
  }, 500);

  const handleSpeedChange = (value: string) => {
    setSpeed(value);
    submitSpeed(value);
  };

  const handleFrequencyChange = (value: string) => {
    setFrequency(value);
    submitFrequency(value);
  };

  const handleTransitionChange = (value: string) => {
    setTransition(value);
    submitTransition(value);
  };

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 bg-gray-50">
      <div className="px-8 py-8 flex items-center justify-center">
        <div className="max-w-md w-full space-y-8">
          <Button
            label="Raise Desk"
            onMouseDown={raiseDesk}
            onTouchStart={raiseDesk}
            onMouseUp={stopDesk}
            onTouchEnd={stopDesk}
          />
          <Button
            label="Lower Desk"
            onMouseDown={lowerDesk}
            onTouchStart={lowerDesk}
            onMouseUp={stopDesk}
            onTouchEnd={stopDesk}
          />
          <Button label="Start Motor" onClick={raiseDesk} />
          <Button label="Stop Motor" onClick={stopDesk} />
          <div className="grid grid-cols-6 gap-6">
            <div className="col-span-6 sm:col-span-3">
              <FormInput
                type="number"
                min="0"
                max="100"
                step="5"
                label="Speed (%)"
                value={speed}
                onChange={handleSpeedChange}
              />
            </div>
            <div className="col-span-6 sm:col-span-3">
              <FormInput
                type="number"
                min="100"
                max="10000"
                step="10"
                label="PWM Frequency (Hz)"
                value={frequency}
                onChange={handleFrequencyChange}
              />
            </div>
            <div className="col-span-6 sm:col-span-3">
              <FormInput
                type="number"
                min="0"
                max="30"
                step="0.5"
                label="Transition Time (sec)"
                value={transition}
                onChange={handleTransitionChange}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
