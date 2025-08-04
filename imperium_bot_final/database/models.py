"""
Modelo do banco de dados SQLite para o Imperium™ Bot
Contém todas as tabelas necessárias para operação completa do sistema
"""

import aiosqlite
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os

DATABASE_PATH = "imperium_bot.db"

class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
    
    async def init_database(self):
        """Inicializa o banco de dados criando todas as tabelas necessárias"""
        async with aiosqlite.connect(self.db_path) as db:
            # Tabela de usuários
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    referrer_id INTEGER,
                    is_admin INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    FOREIGN KEY (referrer_id) REFERENCES users (user_id)
                )
            """)
            
            # Tabela de assinaturas
            await db.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    plan_name TEXT NOT NULL,
                    plan_price REAL NOT NULL,
                    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_date DATETIME NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    payment_id TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Tabela de vendas de afiliados
            await db.execute("""
                CREATE TABLE IF NOT EXISTS affiliate_sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    affiliate_id INTEGER,
                    referred_user_id INTEGER,
                    subscription_id INTEGER,
                    commission_amount REAL NOT NULL,
                    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    commission_paid INTEGER DEFAULT 0,
                    FOREIGN KEY (affiliate_id) REFERENCES users (user_id),
                    FOREIGN KEY (referred_user_id) REFERENCES users (user_id),
                    FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
                )
            """)
            
            # Tabela de solicitações de saque
            await db.execute("""
                CREATE TABLE IF NOT EXISTS withdrawal_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL NOT NULL,
                    pix_key TEXT NOT NULL,
                    pix_key_type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed_date DATETIME,
                    processed_by INTEGER,
                    rejection_reason TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (processed_by) REFERENCES users (user_id)
                )
            """)
            
            # Tabela de pagamentos
            await db.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    mp_payment_id TEXT UNIQUE,
                    amount REAL NOT NULL,
                    plan_name TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    qr_code_data TEXT,
                    qr_code_base64 TEXT,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expiration_date DATETIME,
                    approval_date DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Tabela de configurações do sistema
            await db.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    description TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Inserir configurações padrão se não existirem
            default_configs = [
                ('commission_rate', '0.20', 'Taxa de comissão para afiliados (20%)'),
                ('min_withdrawal', '50.00', 'Valor mínimo para saque (R$ 50,00)'),
                ('payment_expiration_hours', '24', 'Horas para expiração de pagamento Pix'),
                ('vip_group_link', 'https://t.me/seu_grupo_vip', 'Link do grupo VIP'),
                ('support_contact', '@seu_suporte', 'Contato de suporte')
            ]
            
            for key, value, description in default_configs:
                await db.execute("""
                    INSERT OR IGNORE INTO system_config (key, value, description)
                    VALUES (?, ?, ?)
                """, (key, value, description))
            
            await db.commit()
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                      last_name: str = None, referrer_id: int = None) -> bool:
        """Adiciona um novo usuário ao banco de dados"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR IGNORE INTO users 
                    (user_id, username, first_name, last_name, referrer_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, username, first_name, last_name, referrer_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Busca um usuário pelo ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM users WHERE user_id = ?
                """, (user_id,))
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
    
    async def update_user_phone(self, user_id: int, phone: str) -> bool:
        """Atualiza o telefone do usuário"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE users SET phone = ? WHERE user_id = ?
                """, (phone, user_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar telefone: {e}")
            return False
    
    async def create_subscription(self, user_id: int, plan_name: str, plan_price: float, 
                                duration_days: int, payment_id: str = None) -> int:
        """Cria uma nova assinatura"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                end_date = datetime.now() + timedelta(days=duration_days)
                cursor = await db.execute("""
                    INSERT INTO subscriptions 
                    (user_id, plan_name, plan_price, end_date, payment_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, plan_name, plan_price, end_date, payment_id))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar assinatura: {e}")
            return 0
    
    async def get_active_subscription(self, user_id: int) -> Optional[Dict]:
        """Busca assinatura ativa do usuário"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM subscriptions 
                    WHERE user_id = ? AND is_active = 1 AND end_date > CURRENT_TIMESTAMP
                    ORDER BY end_date DESC LIMIT 1
                """, (user_id,))
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Erro ao buscar assinatura: {e}")
            return None
    
    async def create_payment(self, user_id: int, mp_payment_id: str, amount: float, 
                           plan_name: str, qr_code_data: str, qr_code_base64: str) -> bool:
        """Cria um registro de pagamento"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                expiration_date = datetime.now() + timedelta(hours=24)
                await db.execute("""
                    INSERT INTO payments 
                    (user_id, mp_payment_id, amount, plan_name, qr_code_data, 
                     qr_code_base64, expiration_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, mp_payment_id, amount, plan_name, qr_code_data, 
                      qr_code_base64, expiration_date))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao criar pagamento: {e}")
            return False
    
    async def get_payment(self, mp_payment_id: str) -> Optional[Dict]:
        """Busca um pagamento pelo ID do Mercado Pago"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM payments WHERE mp_payment_id = ?
                """, (mp_payment_id,))
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Erro ao buscar pagamento: {e}")
            return None
    
    async def update_payment_status(self, mp_payment_id: str, status: str) -> bool:
        """Atualiza o status de um pagamento"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                approval_date = datetime.now() if status == 'approved' else None
                await db.execute("""
                    UPDATE payments 
                    SET status = ?, approval_date = ?
                    WHERE mp_payment_id = ?
                """, (status, approval_date, mp_payment_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar status do pagamento: {e}")
            return False
    
    async def create_affiliate_sale(self, affiliate_id: int, referred_user_id: int, 
                                  subscription_id: int, commission_amount: float) -> bool:
        """Registra uma venda de afiliado"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO affiliate_sales 
                    (affiliate_id, referred_user_id, subscription_id, commission_amount)
                    VALUES (?, ?, ?, ?)
                """, (affiliate_id, referred_user_id, subscription_id, commission_amount))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao registrar venda de afiliado: {e}")
            return False
    
    async def get_affiliate_balance(self, user_id: int) -> float:
        """Calcula o saldo disponível do afiliado"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Saldo total de comissões
                cursor = await db.execute("""
                    SELECT COALESCE(SUM(commission_amount), 0) as total_commission
                    FROM affiliate_sales WHERE affiliate_id = ?
                """, (user_id,))
                total_commission = (await cursor.fetchone())[0]
                
                # Saques aprovados
                cursor = await db.execute("""
                    SELECT COALESCE(SUM(amount), 0) as total_withdrawn
                    FROM withdrawal_requests 
                    WHERE user_id = ? AND status = 'approved'
                """, (user_id,))
                total_withdrawn = (await cursor.fetchone())[0]
                
                return total_commission - total_withdrawn
        except Exception as e:
            print(f"Erro ao calcular saldo do afiliado: {e}")
            return 0.0
    
    async def create_withdrawal_request(self, user_id: int, amount: float, 
                                      pix_key: str, pix_key_type: str) -> bool:
        """Cria uma solicitação de saque"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO withdrawal_requests 
                    (user_id, amount, pix_key, pix_key_type)
                    VALUES (?, ?, ?, ?)
                """, (user_id, amount, pix_key, pix_key_type))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao criar solicitação de saque: {e}")
            return False
    
    async def get_pending_withdrawals(self) -> List[Dict]:
        """Busca todas as solicitações de saque pendentes"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT wr.*, u.first_name, u.username
                    FROM withdrawal_requests wr
                    JOIN users u ON wr.user_id = u.user_id
                    WHERE wr.status = 'pending'
                    ORDER BY wr.request_date ASC
                """)
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar saques pendentes: {e}")
            return []
    
    async def process_withdrawal(self, withdrawal_id: int, status: str, 
                               processed_by: int, rejection_reason: str = None) -> bool:
        """Processa uma solicitação de saque"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE withdrawal_requests 
                    SET status = ?, processed_date = CURRENT_TIMESTAMP, 
                        processed_by = ?, rejection_reason = ?
                    WHERE id = ?
                """, (status, processed_by, rejection_reason, withdrawal_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"Erro ao processar saque: {e}")
            return False
    
    async def get_system_config(self, key: str) -> Optional[str]:
        """Busca uma configuração do sistema"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT value FROM system_config WHERE key = ?
                """, (key,))
                row = await cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            print(f"Erro ao buscar configuração: {e}")
            return None
    
    async def get_statistics(self) -> Dict:
        """Busca estatísticas gerais do sistema"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                stats = {}
                
                # Total de usuários
                cursor = await db.execute("SELECT COUNT(*) FROM users")
                stats['total_users'] = (await cursor.fetchone())[0]
                
                # Usuários hoje
                cursor = await db.execute("""
                    SELECT COUNT(*) FROM users 
                    WHERE DATE(registration_date) = DATE('now')
                """)
                stats['users_today'] = (await cursor.fetchone())[0]
                
                # Assinaturas ativas
                cursor = await db.execute("""
                    SELECT COUNT(*) FROM subscriptions 
                    WHERE is_active = 1 AND end_date > CURRENT_TIMESTAMP
                """)
                stats['active_subscriptions'] = (await cursor.fetchone())[0]
                
                # Faturamento total
                cursor = await db.execute("""
                    SELECT COALESCE(SUM(plan_price), 0) FROM subscriptions
                """)
                stats['total_revenue'] = (await cursor.fetchone())[0]
                
                # Faturamento hoje
                cursor = await db.execute("""
                    SELECT COALESCE(SUM(plan_price), 0) FROM subscriptions
                    WHERE DATE(start_date) = DATE('now')
                """)
                stats['revenue_today'] = (await cursor.fetchone())[0]
                
                # Saques pendentes
                cursor = await db.execute("""
                    SELECT COUNT(*) FROM withdrawal_requests WHERE status = 'pending'
                """)
                stats['pending_withdrawals'] = (await cursor.fetchone())[0]
                
                return stats
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}

# Instância global do banco de dados
db_manager = DatabaseManager()