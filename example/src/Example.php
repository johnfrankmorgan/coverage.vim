<?php

namespace Example;

class Example
{
    public function doSomething(int $number): bool
    {
        if ($number > 100) {
            return true;
        }

        return false;
    }
}
