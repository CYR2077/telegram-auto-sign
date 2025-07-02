import asyncio
import os
import logging
import json
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
    
    # 使用JSON格式配置
    # SIGN_CONFIG格式: {"target1": "message1", "target2": "message2"}
    SIGN_CONFIG = os.getenv('SIGN_CONFIG', '{}')
    
    logger.info(f"🚀 开始发送消息任务 - {datetime.now()}")
    
    # 解析JSON配置
    try:
        target_messages = json.loads(SIGN_CONFIG)
        if not target_messages:
            logger.error("❌ SIGN_CONFIG 配置为空，请设置签到目标")
            return
        logger.info("📋 使用JSON格式配置")
            
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON配置解析失败: {e}")
        logger.error("💡 配置格式示例: '{\"@bot1\": \"/sign\", \"@bot2\": \"/checkin\"}'")
        return
    except Exception as e:
        logger.error(f"❌ 配置解析失败: {e}")
        return
    
    if not target_messages:
        logger.error("❌ 没有找到有效的签到目标")
        return
    
    logger.info(f"📝 配置的发送目标: {list(target_messages.keys())}")
    
    # 创建客户端
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    try:
        await client.start()
        
        # 获取用户信息
        me = await client.get_me()
        logger.info(f"✅ 登录成功: {me.first_name}")
        
        success_count = 0
        total_count = len(target_messages)
        
        # 执行签到
        for target, message in target_messages.items():
            try:
                await client.send_message(target, message)
                logger.info(f"✅ 发送成功: {target} -> {message}")
                success_count += 1
            except Exception as e:
                logger.error(f"❌ 发送失败 {target}: {e}")
            
            # 延迟避免频率限制
            await asyncio.sleep(3)
        
        logger.info(f"📊 发送完成: {success_count}/{total_count} 成功")
        
    except Exception as e:
        logger.error(f"💥 程序错误: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(auto_sign())
