let &runtimepath.=','.escape(expand('<sfile>:p:h') . '/..', '\,')

augroup reload
  autocmd!
  autocmd BufWritePost *.py UpdateRemotePlugins
augroup END
