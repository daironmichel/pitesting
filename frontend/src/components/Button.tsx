import * as React from "react";

type Props = {
  label: string;
  onClick?: (event: React.SyntheticEvent<HTMLButtonElement>) => void;
  onMouseDown?: (event: React.SyntheticEvent<HTMLButtonElement>) => void;
  onMouseUp?: (event: React.SyntheticEvent<HTMLButtonElement>) => void;
  onTouchStart?: (event: React.SyntheticEvent<HTMLButtonElement>) => void;
  onTouchEnd?: (event: React.SyntheticEvent<HTMLButtonElement>) => void;
};

function Button(props: React.PropsWithChildren<Props>): JSX.Element {
  const { label, children, ...events } = props;
  return (
    <button
      {...events}
      className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      {label}
      {children}
    </button>
  );
}

export default Button;
