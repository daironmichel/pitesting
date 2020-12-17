import React, { SyntheticEvent } from "react";

type Props = {
  id?: string;
  name?: string;
  autoComplete?: string;
  type?: "text" | "number" | "checkbox" | "radio";
  placeholder?: string;
  step?: string | number;
  min?: string | number;
  max?: string | number;
  label: string;
  value: string;
  onChange: (value: string) => void;
};

function FormInput(props: Props): JSX.Element {
  const valueChanged = (e: SyntheticEvent<HTMLInputElement>) => {
    props.onChange(e.currentTarget.value);
  };

  return (
    <>
      <label
        htmlFor="first_name"
        className="block text-sm font-medium text-gray-700"
      >
        {props.label}
      </label>
      <input
        type={props.type || "text"}
        name={props.name}
        id={props.id}
        autoComplete={props.autoComplete}
        step={props.step}
        min={props.min}
        max={props.max}
        className="p-2 mt-1 border-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        value={props.value}
        onChange={valueChanged}
      />
    </>
  );
}

export default FormInput;
