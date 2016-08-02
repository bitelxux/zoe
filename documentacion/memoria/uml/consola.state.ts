participant Usuario

title State

Usuario->Consola: state [for] [texto]
alt No se indica for ni texto
    Consola->Usuario: Estado actual general
done

alt Se indica for pero no texto
    Consola->Usuario: Estado actual para el <for> indicado 
done

alt Se indica for y texto
    Consola->Usuario: se establece el estado <texto> para el destino <for>
done

Consola->Usuario: Resultado

