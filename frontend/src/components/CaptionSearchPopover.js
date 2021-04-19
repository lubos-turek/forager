import React, { useState, useEffect, useRef } from "react";
import {
  Popover,
  PopoverBody,
  Button,
  Input,
} from "reactstrap";
import Emoji from "react-emoji-render";

import fromPairs from "lodash/fromPairs";
import toPairs from "lodash/toPairs";

const endpoints = fromPairs(toPairs({
  generateTextEmbedding: 'generate_text_embedding_v2',
}).map(([name, endpoint]) => [name, `${process.env.REACT_APP_SERVER_URL}/api/${endpoint}`]));

const CaptionSearchPopover = ({ text, setText, textEmbedding, setTextEmbedding }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const textAreaRef = useRef();

  const setTextFromLink = (e, text) => {
    setText(text);
    e.preventDefault();
    textAreaRef.current.focus();
    textAreaRef.current.selectionStart = text.length;
    textAreaRef.current.selectionEnd = text.length;
  }

  const generateEmbedding = async () => {
    const url = new URL(endpoints.generateTextEmbedding);
    const body = { text };

    const res = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body),
    }).then(res => res.json());
    setTextEmbedding(res.embedding);
  }

  useEffect(() => {
    if (isLoading) generateEmbedding().finally(() => setIsLoading(false));
  }, [isLoading]);

  return (
    <Popover
      placement="bottom"
      isOpen={isOpen}
      target="ordering-mode"
      trigger="hover"
      toggle={() => setIsOpen(!isOpen)}
      fade={false}
      popperClassName={`caption-search-popover ${isLoading ? "loading" : ""}`}
    >
      <PopoverBody>
        <p className="mt-1">
          Good queries generally begin with:
          <ul className="pl-3 text-secondary">
            <li>
              <a
                href="#"
                onClick={e => setTextFromLink(e, "A photo of a ")}
                className="text-secondary"
              >
                A photo of a(n)...
              </a>
            </li>
            <li>
              <a
                href="#"
                onClick={e => setTextFromLink(e, "A photo containing a ")}
                className="text-secondary"
              >
                A photo containing a(n)...
              </a>
            </li>
          </ul>
        </p>
        <Input
          autoFocus
          innerRef={textAreaRef}
          type="textarea"
          value={text}
          onChange={e => {
            setText(e.target.value.replace("\n", " "));
            setTextEmbedding("");
          }}
          placeholder="Caption"
          disabled={isLoading}
        />
        <Button
          color="light"
          onClick={() => setIsLoading(true)}
          disabled={text.trim().length === 0 || isLoading || textEmbedding}
          className="mt-2 mb-1 w-100"
        >{textEmbedding ? <>
          <Emoji text=":white_check_mark:"/> Ready to query
        </> : "Generate embedding"}</Button>
      </PopoverBody>
    </Popover>
  );
};

export default CaptionSearchPopover;
