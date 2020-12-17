import React from "react";
import axios from "axios";
import Button from "../components/Button";

function Dashboard() {
  const axiosInstance = axios.create({ baseURL: window.location.origin });
  const raiseDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/up");
    } catch (e) {
      console.error(e);
    }
  };

  const lowerDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/down");
    } catch (e) {
      console.error(e);
    }
  };

  const stopDesk = async () => {
    try {
      await axiosInstance.post("/api/desk/stop");
    } catch (e) {
      console.error(e);
    }
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
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
