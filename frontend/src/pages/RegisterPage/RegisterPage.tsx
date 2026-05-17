import type { FormProps } from "antd";
import { Button, Form, Input, Typography } from "antd";
import { Link } from "react-router-dom";

const { Text, Title } = Typography;

import { US_API_URL, ACCESS_TOKEN } from "../../constants";

import styles from "./RegisterPage.module.css";
import { useState } from "react";

type FieldType = {
  email?: string;
  password?: string;
};

interface AuthServerResponse {
  status: boolean;
  access_token: string;
}

const onFinishFailed: FormProps<FieldType>["onFinishFailed"] = (errorInfo) => {
  console.log("Failed:", errorInfo);
};

function RegisterPage() {
  const [error, setError] = useState<string>();
  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    const url = US_API_URL + "/users/register";
    const body = JSON.stringify(values);
    const response = await fetch(url, {
      method: "POST",
      body,
      headers: {
        "Content-type": "application/json",
      },
    });
    if (response.ok) {
      const data: AuthServerResponse = await response.json();
      localStorage.setItem(ACCESS_TOKEN, data.access_token);
      window.location.href = "/";
    } else {
      if (response.status === 409) {
        setError("Email already registered.");
      }
    }
  };
  return (
    <div className={styles["container"]}>
      <Form
        className={styles["form"]}
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Title>Register</Title>
        <Form.Item<FieldType>
          label="Email"
          name="email"
          rules={[{ required: true, message: "Please input your email!" }]}
        >
          <Input size="large" />
        </Form.Item>

        <Form.Item<FieldType>
          label="Password"
          name="password"
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input.Password size="large" />
        </Form.Item>

        <Text type={"danger"}>{error}</Text>

        <Form.Item label={null}>
          <Button type="primary" htmlType="submit" size="large">
            Register
          </Button>
        </Form.Item>
      </Form>
      <Link to={"/login"} className={styles["link"]}>
        <Text type="secondary" className={styles["text"]}>
          Already have an account?
        </Text>
      </Link>
    </div>
  );
}

export default RegisterPage;
