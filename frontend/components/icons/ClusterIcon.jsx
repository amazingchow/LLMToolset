import React from 'react';

// 使用 forwardRef 可以让你像对DOM元素一样传递 ref
const ClusterIcon = React.forwardRef(({ color = 'currentColor', size = 32, ...props }, ref) => (
  <svg
    ref={ref}
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill={color} // 使用 color prop 来控制填充色
    {...props}
  >
    <g id="server-cluster">
      <g>
        <path d="M24,23H0V0h24V23z M2,21h20v-5H2V21z M2,14h20V9H2V14z M2,7h20V2H2V7z" />
      </g>
      <g>
        <rect x="13" y="3" width="2" height="3" />
      </g>
      <g>
        <rect x="16" y="3" width="2" height="3" />
      </g>
      <g>
        <rect x="19" y="3" width="2" height="3" />
      </g>
      <g>
        <rect x="13" y="10" width="2" height="3" />
      </g>
      <g>
        <rect x="16" y="10" width="2" height="3" />
      </g>
      <g>
        <rect x="19" y="10" width="2" height="3" />
      </g>
      <g>
        <rect x="13" y="17" width="2" height="3" />
      </g>
      <g>
        <rect x="16" y="17" width="2" height="3" />
      </g>
      <g>
        <rect x="19" y="17" width="2" height="3" />
      </g>
    </g>
  </svg>
));

export default ClusterIcon;
