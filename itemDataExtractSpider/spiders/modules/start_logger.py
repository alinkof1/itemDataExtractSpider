import logging

def start_log():
	#Debug Logging information
	_NAME = 'link_extractor'
	logging.basicConfig(level=logging.DEBUG,disable_existing_loggers= False)
	logger = logging.getLogger(_NAME)
	
	if __name__ == '__main__':
		handler = logging.FileHandler('logs/%s.log' % _NAME)
	else:
		handler = logging.FileHandler('spiders/modules/logs/%s.log' % _NAME)
		#handler = logging.FileHandler('logs/%s.log' % _NAME)
		
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
    
	logger.info('-----------------------------------------------')
	logger.info('creating search class')
	return logger