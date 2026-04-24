import { useState } from "react";

import { Button } from "antd";
import copy_icon_white from "/copy_icon_white.svg";

interface CopyBtnProps {
  textToCopy: string;
}

function CopyBtn(props: CopyBtnProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(props.textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Button type={copied ? "primary" : "default"} onClick={handleCopy}>
      <img src={copy_icon_white} alt="" />
    </Button>
  );
}

export default CopyBtn;
