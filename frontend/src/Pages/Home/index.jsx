import React, { useState } from 'react';
import {
  Container,
  TopButtons,
  UploadLabel,
  HiddenInput,
  Button,
  MainContent,
  ImageArea,
  ImageWrapper,
  PreviewImage,
  Placeholder,
  SlidersBlock,
  SliderGroup,
  SliderLabel,
  Slider,
  ArrowForwardButton,
  ArrowBackButton,
} from './styles';
import axios from 'axios';

export default function PhotoUploadPage() {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [imageId, setImageId] = useState(null);
  const [filters, setFilters] = useState({
    brightness: 1,
    contrast: 1,
    sharpness: 1,
    color: 1,
    blur: 0,
    gamma: 1,
    sepia: 0,
    temperature: 5000,
    exposure: 0,
    hue: 0,
  });

  const handleUpload = async (e) => {
  const selectedFile = e.target.files[0];
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await axios.post('http://localhost/upload', formData);

    console.log('Ответ сервера:', response.data);

    setImageId(response.data.image_id);

    if (response.data.image_url) {
      setPreviewUrl(response.data.image_url);
      console.log(response.data.image_url);
    } else {
      setPreviewUrl(URL.createObjectURL(selectedFile));
    }

    console.log('Изображение успешно загружено');
  } catch (error) {
    console.error('Ошибка при загрузке:', error);
    alert('Ошибка при загрузке изображения');
  }
};


  const handleFilterChange = (type, value) => {
    setFilters((prev) => ({ ...prev, [type]: value }));
  };

  const getCssFilterString = () => {
    return `
      brightness(${filters.brightness})
      contrast(${filters.contrast})
      saturate(${filters.color})
      sepia(${filters.sepia})
      blur(${filters.blur}px)
      hue-rotate(${filters.hue}deg)
    `;
  };
  function parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = decodeURIComponent(atob(base64Url).split('').map(c =>
          '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      ).join(''));
      return JSON.parse(base64);
    } catch (e) {
      console.error('Не удалось распарсить токен:', e);
      return null;
    }
  }


  const handleSave = async () => {
  if (!imageId) {
    alert('Сначала загрузите изображение.');
    return;
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Токен не найден. Авторизуйтесь.');
    return;
  }

  const payload = parseJwt(token);
  const userId = payload?.user_id;
  console.log(userId)
  if (!userId) {
    alert('Не удалось получить user_id из токена');
    return;
  }

  try {
    const filtersArray = Object.entries(filters).map(([type, value]) => ({
      type,
      value,
    }));

    const response = await axios.post('http://localhost/editphoto/filter/', {
  user_id: userId,
  image_url: previewUrl,
  filters: filtersArray,
});

    if (response.data.filtered_url) {
      window.open(response.data.filtered_url, '_blank');
    } else {
      alert('Не удалось сохранить изображение.');
    }
  } catch (error) {
    console.error('Ошибка при сохранении:', error.response?.data || error);
    alert('Произошла ошибка при сохранении изображения');
  }
};



  const renderSlider = (label, type, min, max, step) => (
    <SliderGroup key={type}>
      <SliderLabel>{label}: {filters[type]}</SliderLabel>
      <Slider
        type="range"
        min={min}
        max={max}
        step={step}
        value={filters[type]}
        onChange={(e) => handleFilterChange(type, parseFloat(e.target.value))}
      />
    </SliderGroup>
  );

  return (
    <Container>
      <TopButtons>
        <UploadLabel>
          Загрузить
          <HiddenInput type="file" accept="image/*" onChange={handleUpload} />
        </UploadLabel>
        <ArrowBackButton />
        <ArrowForwardButton />
        <Button onClick={handleSave}>Сохранить</Button>
      </TopButtons>

      <MainContent>
        <ImageArea>
          <ImageWrapper>
            {previewUrl ? (
              <PreviewImage src={previewUrl} alt="Preview" style={{ filter: getCssFilterString() }} />

            ) : (
              <Placeholder>Изображение не загружено</Placeholder>
            )}
          </ImageWrapper>

          <SlidersBlock>
            {renderSlider("Яркость", "brightness", 0.0, 2.0, 0.01)}
            {renderSlider("Контраст", "contrast", 0.0, 2.0, 0.01)}
            {renderSlider("Резкость", "sharpness", 0.0, 2.0, 0.01)}
            {renderSlider("Насыщ. цвета", "color", 0.0, 2.0, 0.01)}
            {renderSlider("Размытие", "blur", 0.0, 10.0, 0.1)}
            {renderSlider("Гамма", "gamma", 0.5, 2.5, 0.1)}
            {renderSlider("Сепия", "sepia", 0.0, 1.0, 0.01)}
            {renderSlider("Температура", "temperature", 3000, 8000, 100)}
            {renderSlider("Экспозиция", "exposure", -1.0, 1.0, 0.01)}
            {renderSlider("Оттенок", "hue", 0, 360, 1)}
          </SlidersBlock>
        </ImageArea>
      </MainContent>
    </Container>
  );
}
