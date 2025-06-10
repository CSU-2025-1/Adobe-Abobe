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
  const [loading, setLoading] = useState(false);
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

  const defaultValues = {
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
  };

  const handleUpload = async (e) => {
  const selectedFile = e.target.files[0];
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await axios.post('http://localhost/image/upload', formData);

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
  if (!userId) {
    alert('Не удалось получить user_id из токена');
    return;
  }

  try {
    const filtersArray = Object.entries(filters)
      .filter(([key, value]) => value !== defaultValues[key])
      .map(([type, value]) => ({ type, value })
    );

    setLoading(true);
    console.log(filtersArray)

    const response = await axios.post('http://localhost/image/filter', {
      user_id: 0,
      image_url: previewUrl.replace('localhost', 'minio'),
      filters: filtersArray,
    });

    const taskId = response.data.task_id;

    let retries = 0;
    const maxRetries = 20;

    const pollForResult = async () => {
      try {
        const resultResponse = await axios.get(`http://localhost/image/operations/${taskId}`);
        if (resultResponse.data.status === 'done') {
          setLoading(false);

          const filteredUrl = resultResponse.data.filtered_url;

          // Сохраняем историю
          const timestamp = new Date().toISOString();
          const historyEntry = {
            timestamp,
            filters: filtersArray,
            image_url: filteredUrl
          };
          localStorage.setItem(`history_${taskId}`, JSON.stringify(historyEntry));

          const response = await fetch(filteredUrl, {
            mode: 'cors',
          });
          const blob = await response.blob();

          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = 'filtered.jpg';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } else if (retries < maxRetries) {
          retries++;
          setTimeout(pollForResult, 500);
        } else {
          setLoading(false);
          alert("Обработка заняла слишком много времени");
        }
      } catch (err) {
        setLoading(false);
        alert("Ошибка при получении результата");
      }
    };

    pollForResult();

  } catch (error) {
    setLoading(false);
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
   <>
      {loading && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '24px',
          fontWeight: 'bold'
        }}>
          Обработка изображения...
        </div>
      )}
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
   </>
  );
}
