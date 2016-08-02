participant Usuario

title Avatar

Usuario->Consola: avatar [for] [path]
alt No se indica for ni path
    Consola->Usuario: avatar actual general
done

alt Se indica for pero no avatar
    Consola->Usuario: Avatar actual para el <for> indicado 
done

alt Se indica for y path
    Consola->Usuario: se establece el avatar <path> para el destino <for>
done

Consola->Usuario: Resultado

