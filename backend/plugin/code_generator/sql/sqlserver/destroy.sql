DELETE FROM sys_menu WHERE name IN ('AddGenCodeBusiness', 'EditGenCodeBusiness', 'DeleteGenCodeBusiness', 'AddGenCodeModel', 'EditGenCodeModel', 'DeleteGenCodeModel', 'ImportGenCode', 'WriteGenCode');

DELETE FROM sys_menu WHERE name = 'PluginCodeGenerator';

DROP TABLE IF EXISTS gen_column;
DROP TABLE IF EXISTS gen_business;
