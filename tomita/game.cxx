#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики

Name -> Word<h-reg1, ~fw, nc-agr[1]> Word<h-reg1, nc-agr[1]>*;

S -> Name interp (Game.Name::not_norm);