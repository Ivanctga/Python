"""
Gerador de QR Code com fallback multiplataforma
Compatível com Linux, Termux, macOS e Windows
"""

import qrcode
import qrcode.image.svg
import base64
import io
import os
import platform
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
from utils.logger import logger

class QRCodeGenerator:
    def __init__(self):
        """Inicializa o gerador de QR Code"""
        self.system = platform.system().lower()
        logger.info(f"QR Code Generator inicializado para sistema: {self.system}")
    
    def generate_qr_code(self, data: str, logo_path: str = None) -> Optional[bytes]:
        """
        Gera QR Code como imagem bytes
        
        Args:
            data: Dados para o QR Code (código Pix)
            logo_path: Caminho para logo a ser inserido no centro (opcional)
        
        Returns:
            Bytes da imagem do QR Code ou None se erro
        """
        try:
            # Configurações do QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta correção para logo
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Gerar imagem do QR Code
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Adicionar logo se fornecido e arquivo existir
            if logo_path and os.path.exists(logo_path):
                qr_img = self._add_logo_to_qr(qr_img, logo_path)
            
            # Converter para bytes
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG', quality=95)
            img_bytes = img_buffer.getvalue()
            
            logger.info("QR Code gerado com sucesso")
            return img_bytes
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code: {e}")
            return self._generate_fallback_qr(data)
    
    def generate_qr_with_info(self, pix_data: str, amount: float, 
                             description: str = "Imperium™") -> Optional[bytes]:
        """
        Gera QR Code com informações adicionais
        
        Args:
            pix_data: Código Pix
            amount: Valor do pagamento
            description: Descrição do pagamento
        
        Returns:
            Bytes da imagem do QR Code com informações
        """
        try:
            # Gerar QR Code básico
            qr_bytes = self.generate_qr_code(pix_data)
            if not qr_bytes:
                return None
            
            # Carregar imagem do QR Code
            qr_image = Image.open(io.BytesIO(qr_bytes))
            
            # Criar imagem maior com informações
            final_image = self._add_payment_info(qr_image, amount, description)
            
            # Converter para bytes
            img_buffer = io.BytesIO()
            final_image.save(img_buffer, format='PNG', quality=95)
            
            logger.info("QR Code com informações gerado com sucesso")
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code com informações: {e}")
            return self.generate_qr_code(pix_data)
    
    def _add_logo_to_qr(self, qr_img: Image.Image, logo_path: str) -> Image.Image:
        """
        Adiciona logo ao centro do QR Code
        
        Args:
            qr_img: Imagem do QR Code
            logo_path: Caminho para o logo
        
        Returns:
            Imagem do QR Code com logo
        """
        try:
            # Abrir logo
            logo = Image.open(logo_path)
            
            # Calcular tamanho do logo (10% do QR Code)
            qr_width, qr_height = qr_img.size
            logo_size = min(qr_width, qr_height) // 10
            
            # Redimensionar logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Criar máscara circular para o logo
            mask = Image.new('L', (logo_size, logo_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo_size, logo_size), fill=255)
            
            # Aplicar máscara
            logo.putalpha(mask)
            
            # Calcular posição central
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # Colar logo no QR Code
            qr_img.paste(logo, logo_pos, logo)
            
            return qr_img
            
        except Exception as e:
            logger.warning(f"Erro ao adicionar logo ao QR Code: {e}")
            return qr_img
    
    def _add_payment_info(self, qr_image: Image.Image, amount: float, 
                         description: str) -> Image.Image:
        """
        Adiciona informações de pagamento à imagem do QR Code
        
        Args:
            qr_image: Imagem do QR Code
            amount: Valor do pagamento
            description: Descrição
        
        Returns:
            Imagem final com informações
        """
        try:
            qr_width, qr_height = qr_image.size
            
            # Criar imagem maior para incluir texto
            padding = 100
            final_width = qr_width + (padding * 2)
            final_height = qr_height + padding + 150  # Espaço extra para texto
            
            # Criar imagem final com fundo branco
            final_image = Image.new('RGB', (final_width, final_height), 'white')
            
            # Colar QR Code no centro
            qr_pos = (padding, padding)
            final_image.paste(qr_image, qr_pos)
            
            # Adicionar texto
            draw = ImageDraw.Draw(final_image)
            
            # Tentar carregar fonte
            font_large = self._get_font(24)
            font_medium = self._get_font(18)
            font_small = self._get_font(14)
            
            # Texto do título
            title_text = description
            title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (final_width - title_width) // 2
            draw.text((title_x, 20), title_text, fill='black', font=font_large)
            
            # Texto do valor
            value_text = f"R$ {amount:.2f}".replace(".", ",")
            value_bbox = draw.textbbox((0, 0), value_text, font=font_medium)
            value_width = value_bbox[2] - value_bbox[0]
            value_x = (final_width - value_width) // 2
            draw.text((value_x, 50), value_text, fill='green', font=font_medium)
            
            # Instrução
            instruction_text = "Escaneie com seu app bancário"
            instruction_bbox = draw.textbbox((0, 0), instruction_text, font=font_small)
            instruction_width = instruction_bbox[2] - instruction_bbox[0]
            instruction_x = (final_width - instruction_width) // 2
            draw.text((instruction_x, final_height - 40), instruction_text, fill='gray', font=font_small)
            
            return final_image
            
        except Exception as e:
            logger.warning(f"Erro ao adicionar informações de pagamento: {e}")
            return qr_image
    
    def _get_font(self, size: int) -> ImageFont.ImageFont:
        """
        Obtém fonte com fallback multiplataforma
        
        Args:
            size: Tamanho da fonte
        
        Returns:
            Objeto de fonte
        """
        try:
            # Tentar fontes por sistema operacional
            font_paths = []
            
            if self.system == "windows":
                font_paths = [
                    "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/calibri.ttf",
                    "C:/Windows/Fonts/tahoma.ttf"
                ]
            elif self.system == "darwin":  # macOS
                font_paths = [
                    "/System/Library/Fonts/Arial.ttf",
                    "/System/Library/Fonts/Helvetica.ttc",
                    "/Library/Fonts/Arial.ttf"
                ]
            else:  # Linux e Termux
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/TTF/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/system/fonts/DroidSans.ttf",  # Android/Termux
                    "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf"  # Termux específico
                ]
            
            # Tentar carregar cada fonte
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            
            # Fallback para fonte padrão
            return ImageFont.load_default()
            
        except Exception as e:
            logger.warning(f"Erro ao carregar fonte: {e}")
            return ImageFont.load_default()
    
    def _generate_fallback_qr(self, data: str) -> Optional[bytes]:
        """
        Gera QR Code usando método de fallback mais simples
        
        Args:
            data: Dados para o QR Code
        
        Returns:
            Bytes da imagem ou None se falhar
        """
        try:
            logger.info("Gerando QR Code usando método de fallback")
            
            # QR Code mais simples sem customizações
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=2,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Gerar imagem básica
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            
            logger.info("QR Code de fallback gerado com sucesso")
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Erro no fallback do QR Code: {e}")
            return None
    
    def generate_svg_qr(self, data: str) -> Optional[str]:
        """
        Gera QR Code em formato SVG (útil para casos especiais)
        
        Args:
            data: Dados para o QR Code
        
        Returns:
            String SVG do QR Code ou None se erro
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Gerar SVG
            factory = qrcode.image.svg.SvgPathImage
            svg_img = qr.make_image(image_factory=factory)
            
            # Converter para string
            svg_buffer = io.StringIO()
            svg_img.save(svg_buffer)
            
            logger.info("QR Code SVG gerado com sucesso")
            return svg_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code SVG: {e}")
            return None
    
    def validate_qr_data(self, data: str) -> bool:
        """
        Valida se os dados são adequados para QR Code
        
        Args:
            data: Dados a serem validados
        
        Returns:
            True se válidos, False caso contrário
        """
        try:
            # Verificar tamanho dos dados
            if len(data) > 2000:  # Limite prático para QR Code
                logger.warning("Dados muito longos para QR Code")
                return False
            
            # Verificar se não está vazio
            if not data.strip():
                logger.warning("Dados vazios para QR Code")
                return False
            
            # Tentar gerar QR Code para teste
            test_qr = qrcode.QRCode(version=1)
            test_qr.add_data(data)
            test_qr.make(fit=True)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao validar dados do QR Code: {e}")
            return False

# Instância global do gerador de QR Code
qr_generator = QRCodeGenerator()