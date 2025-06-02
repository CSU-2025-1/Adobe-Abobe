import React, { useState } from "react";
import {
  Container,
  Title,
  Form,
  Input,
  Button,
  ToggleText,
} from "./styles";
import { useNavigate } from "react-router-dom";

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    login: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const url = isLogin
      ? "http://localhost/auth/login"
      : "http://localhost/auth/register";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Что-то пошло не так");
      }

      if (isLogin) {
        localStorage.setItem("isAuthenticated", "true");
        localStorage.setItem("token", data.token);
        navigate("/upload");
      } else {
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Container>
      <Title>{isLogin ? "Вход" : "Регистрация"}</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          name="login"
          placeholder="Логин"
          value={formData.username}
          onChange={handleChange}
        />
        <Input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleChange}
        />
        <Button type="submit">
          {isLogin ? "Войти" : "Зарегистрироваться"}
        </Button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </Form>
      <ToggleText onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Нет аккаунта? Зарегистрироваться" : "Уже есть аккаунт? Войти"}
      </ToggleText>
    </Container>
  );
};

export default AuthPage;
