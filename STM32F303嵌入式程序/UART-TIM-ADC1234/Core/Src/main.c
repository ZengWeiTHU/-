/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <string.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/*���崮�ڽ������ݵĲ���--------------------------------------------------------*/
#define RX_CMD_LEN  1																			//UART_DMA�������鳤��
#define MAX_RX_CMD_LEN  10																//UART���ڽ��ջ������鳤��
unsigned char UART1_Rx_Buf[MAX_RX_CMD_LEN] = {0};					//UART���ڽ��ջ�������
unsigned char UART1_temp[RX_CMD_LEN] = {0};								//UART_DMA��������
unsigned char UART1_Rx_flg = 0;                 					//������һ�������־λ
unsigned int  UART1_Rx_cnt = 0; 													//UART���ڽ��ջ�������index
char airMode;																							//���Ƽ�ѹָ�һ���ֽ�

/*����ADC1��������-------------------------------------------------------------*/
#define BATCH_DATA_LEN 3
uint32_t ADC1_DMA_Buffer[BATCH_DATA_LEN];									//ADC1�������ݻ�������

/*����ADC2���ձ���-------------------------------------------------------------*/
uint32_t ADC2_Value;

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
/*-----------------------------------------------------------------------------
 *��    �ܣ���ѹ����
 *���������pos��mmhg_pressure��pessureValue
 *���������
 *-----------------------------------------------------------------------------*/
void jiaya(int pos,float mmhg_pressure, float pessureValue)
{
	if 			(pos == 1) {HAL_GPIO_WritePin(value1_GPIO_Port,value1_Pin,1);}
  else if (pos == 2) {HAL_GPIO_WritePin(value2_GPIO_Port,value2_Pin,1);}
  else if (pos == 3) {HAL_GPIO_WritePin(value3_GPIO_Port,value3_Pin,1);}
  if (mmhg_pressure > pessureValue)
	{
     if 		 (pos == 1) {HAL_GPIO_WritePin(pump1_GPIO_Port,pump1_Pin,0);}
     else if (pos == 2) {HAL_GPIO_WritePin(pump2_GPIO_Port,pump2_Pin,0);}
     else if (pos == 3) {HAL_GPIO_WritePin(pump3_GPIO_Port,pump3_Pin,0);}
  }
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART1_UART_Init();
  MX_ADC1_Init();
  MX_TIM3_Init();
  MX_ADC2_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */
	HAL_UART_Receive_DMA(&huart1,UART1_temp,RX_CMD_LEN);										//���ڽ�������
	
	HAL_TIM_Base_Start(&htim3);																							//������ʱ��3
	HAL_ADC_Start_DMA(&hadc1,ADC1_DMA_Buffer,BATCH_DATA_LEN);								//ADC1��DMAģʽ��ȡ��ͨ������
	//HAL_ADC_Start_IT(&hadc2);																								//����ADC2���ж�ģʽ
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
		/*------------------------------------------------------------------------------------------------------------------
		 *�ò���Ϊ���������źŲɼ�����ADC2��ADC3��ADC4
		 -------------------------------------------------------------------------------------------------------------------*/
		printf("ADC2:%d",ADC2_Value);
		
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
		/*------------------------------------------------------------------------------------------------------------------
		 *�ò���Ϊ����airMode����ѹ������
		 -------------------------------------------------------------------------------------------------------------------*/
		//printf("ADC1:%d,%d,%d\r\n",ADC1_DMA_Buffer[0],ADC1_DMA_Buffer[1],ADC1_DMA_Buffer[2]);
		
		float ADC1_Channel_1 = (float)ADC1_DMA_Buffer[0]*3.3f/4096;
		float ADC1_Channel_6 = (float)ADC1_DMA_Buffer[1]*3.3f/4096;
		float ADC1_Channel_8 = (float)ADC1_DMA_Buffer[2]*3.3f/4096;
		float mmhg_pressure1 = 106.57 * ADC1_Channel_1 - 19.72;
		float mmhg_pressure2 = 106.57 * ADC1_Channel_6 - 19.72;
		float mmhg_pressure3 = 106.57 * ADC1_Channel_8 - 19.72;
		
		//printf("mmhg_pressure:%f,%f,%f\r\n",mmhg_pressure1,mmhg_pressure2,mmhg_pressure3);
		
		//printf("airMode:%c \r\n",airMode);
		if(UART1_Rx_flg)
		{
			// ҵ����뿪ʼ
			airMode = UART1_Rx_Buf[0];
			printf("You input is:%c \r\n",airMode);

			// ҵ��������
			for(int i = 0; i < UART1_Rx_cnt; i++)   								// ��ս�������
			{
					UART1_Rx_Buf[i] = 0;
			}
			UART1_Rx_cnt = 0;                      									// ��ս��ռ�����
			UART1_Rx_flg = 0;                      									// ��ս�����ɱ�־λ
		}
		
		if ((airMode >=  'a' && airMode <=  'z') || airMode ==  '9')
		{	
			HAL_GPIO_WritePin(pump1_GPIO_Port,pump1_Pin,1);
			HAL_GPIO_WritePin(pump2_GPIO_Port,pump2_Pin,1);
			HAL_GPIO_WritePin(pump3_GPIO_Port,pump3_Pin,1);
		}
		
		switch (airMode){
			 case 'a': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'b': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'c': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'd': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'e': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'f': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'g': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'h': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'i': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 50.0);  break;
			 case 'j': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'k': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'l': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'm': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'n': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'o': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'p': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'q': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 'r': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 100.0); break;
			 case 's': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 150.0); break;
			 case 't': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'u': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 50.0);  jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'v': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'w': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'x': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 100.0); jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'y': jiaya(1, mmhg_pressure1, 50.0);  jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 150.0); break;
			 case 'z': jiaya(1, mmhg_pressure1, 100.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 150.0); break;
			 case '9': jiaya(1, mmhg_pressure1, 150.0); jiaya(2, mmhg_pressure2, 150.0); jiaya(3, mmhg_pressure3, 150.0); break;
		 }
		
		if (airMode == '8')
		{
			HAL_GPIO_WritePin(pump1_GPIO_Port,pump1_Pin,0);
			HAL_GPIO_WritePin(pump2_GPIO_Port,pump2_Pin,0);
			HAL_GPIO_WritePin(pump3_GPIO_Port,pump3_Pin,0);
			HAL_GPIO_WritePin(value1_GPIO_Port,value1_Pin,0);
			HAL_GPIO_WritePin(value2_GPIO_Port,value2_Pin,0);
			HAL_GPIO_WritePin(value3_GPIO_Port,value3_Pin,0);
		}
		
		HAL_Delay(500);																									//��ʱ����

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1|RCC_PERIPHCLK_ADC12
                              |RCC_PERIPHCLK_TIM34;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK2;
  PeriphClkInit.Adc12ClockSelection = RCC_ADC12PLLCLK_DIV1;
  PeriphClkInit.Tim34ClockSelection = RCC_TIM34CLK_HCLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
// �����ض���
int fputc(int ch,FILE *f)
{
	HAL_UART_Transmit_DMA(&huart1,(uint8_t *)&ch,1);
	HAL_Delay(1);
	return 0;
}

//UART_DMA��������жϻص�����
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if(huart->Instance == USART1)
	{
		UART1_Rx_Buf[UART1_Rx_cnt] = UART1_temp[0];
		UART1_Rx_cnt++;
		if(';' == UART1_temp[0])
		{
			UART1_Rx_flg = 1;
		}
		HAL_UART_Receive_DMA(&huart1,UART1_temp,RX_CMD_LEN);
	}
}

//ADCת������жϻص�����
/*
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
	if(hadc->Instance == ADC2)
	{
		ADC2_Value = HAL_ADC_GetValue(hadc);
	}
}
*/
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
