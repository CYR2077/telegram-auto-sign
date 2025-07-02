import asyncio
import os
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

async def auto_sign():
    # 从环境变量获取配置
    API_ID = int(os.getenv('API_ID'))
    API_HASH = os.getenv('API_HASH')
    SESSION_STRING = os.getenv('SESSION_STRING')
    SIGN_TARGETS = os.getenv('SIGN_TARGETS', '').split(',')
    
    logger.info(f"🚀 开始签到任务 - {datetime.now()}")
    
    # 创建客户端
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    try:
        await client.start()
        
        # 获取用户信息
        me = await client.get_me()
        logger.info(f"✅ 登录成功: {me.first_name}")
        
        success_count = 0
        
        # 执行签到
        for target in SIGN_TARGETS:
            target = target.strip()
            if not target:
                continue
                
            try:
                await client.send_message(target, '/sign')
                logger.info(f"✅ 签到成功: {target}")
                success_count += 1
            except Exception as e:
                logger.error(f"❌ 签到失败 {target}: {e}")
            
            # 延迟避免频率限制
            await asyncio.sleep(3)
        
        logger.info(f"📊 签到完成: {success_count}/{len([t for t in SIGN_TARGETS if t.strip()])} 成功")
        
    except Exception as e:
        logger.error(f"💥 程序错误: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(auto_sign())
