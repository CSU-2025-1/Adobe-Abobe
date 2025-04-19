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
    username: "",
    password: "",
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (isLogin) {
      console.log("🔐 Логин", formData);
      localStorage.setItem("isAuthenticated", "true");
      navigate("/upload");
    } else {
      console.log("📝 Регистрация", formData);
      setIsLogin(true);
    }
  };

  return (
    <Container>
      <Title>{isLogin ? "Вход" : "Регистрация"}</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          name="username"
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
      </Form>
      <ToggleText onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Нет аккаунта? Зарегистрироваться" : "Уже есть аккаунт? Войти"}
      </ToggleText>
    </Container>
  );
};

export default AuthPage;
