import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
`;

export const TopButtons = styled.div`
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
`;

export const UploadLabel = styled.label`
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
`;

export const HiddenInput = styled.input`
  display: none;
`;

export const Button = styled.button`
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;

  &:hover {
    background-color: #218838;
  }
`;

export const MainContent = styled.div`
  display: flex;
  width: 100%;
  max-width: 100%;
`;

export const Sidebar = styled.div`
  width: 150px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin-right: 20px;
`;

export const ImageArea = styled.div`
  display: flex;
  align-items: center;
`;

export const ImageWrapper = styled.div`
  width: 1400px;
  height: 700px;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
`;

export const Placeholder = styled.div`
  color: #777;
  font-size: 18px;
`;

export const PreviewImage = styled.img`
  max-width: 100%;
  max-height: 100%;
  display: block;
`;

export const SliderWrapper = styled.div`
  height: 700px;
  display: flex;
  align-items: center;
`;

export const Slider = styled.input`
  writing-mode: bt-lr;
  -webkit-appearance: slider-vertical;
  height: 500px;
  width: 20px;
`;

export const ArrowBackButton = styled.button`
  width: 42px;
  height: 42px;
  background-color: white;
  color: black;
  border: 2px solid #000;
  border-radius: 6px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  &::after {
    content: '';
    display: block;
    margin-left: 4px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 10px solid black;
  }

  &:hover {
    background-color: #f0f0f0;
  }
`;

export const ArrowForwardButton = styled.button`
  width: 42px;
  height: 42px;
  background-color: white;
  color: black;
  border: 2px solid #000;
  border-radius: 6px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  &::after {
    content: '';
    display: block;
    margin-right: 4px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-left: 10px solid black;
  }

  &:hover {
    background-color: #f0f0f0;
  }
`;