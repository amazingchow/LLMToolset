import React from 'react';

// 使用 forwardRef 可以让你像对DOM元素一样传递 ref
const InferIcon = React.forwardRef(({ color = 'currentColor', size = 32, ...props }, ref) => (
  <svg
    ref={ref}
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 16 16"
    fill={color} // 使用 color prop 来控制填充色
    {...props}
  >
    <path d="M13.5 12h-1.793L10 10.293V6.5L9.5 6H8V4h.5l.5-.5v-2L8.5 1h-2l-.5.5v2l.5.5H7v2H5.5l-.5.5v3.793L3.293 12H1.5l-.5.5v2l.5.5h2l.5-.5v-1.793L5.707 11h3.586L11 12.707V14.5l.5.5h2l.5-.5v-2l-.5-.5zM7 2h1v1H7V2zM6 7h3v3H6V7zm-3 7H2v-1h1v1zm10 0h-1v-1h1v1z" />
  </svg>
));

export default InferIcon;
