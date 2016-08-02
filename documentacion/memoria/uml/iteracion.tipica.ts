title Iteración típica de desarrollo

Someone->Trac: Ticket

alt Alguien asigna ticket
  Other->Trac: Assigns ticket 
  Other->Developer: Assigns ticket 
else
  Developer->Trac: Autoassigns ticket
end

Developer->Git: Fetch

Developer->IDE: Solves ticket

Developer->Developer: run tests units
Developer->Developer: check coverage
Developer->Developer: check pylint

alt  ok
  Developer->Git: commit
  Git->Jenkins: Build
else tests fail
  Go to Solves ticket
end

alt Jenkins build pass
  Developer->Jenkins: check pylint
  alt pylint faults
     Developer->Fix faults and recommit
  end
  Developer->Jenkins: check coverage
  alt bad coverage
     Developer->Fix coverage and recommit
  end
else
  Jenkins->Developer: report fail
end

