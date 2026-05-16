import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if(err.status === 0) {
        router.navigate(['/error-page'], {
          state: {
            code: 0
          }
        });
      } else if(err.status === 403) {
        router.navigate(['/error=page']), {
          state: {
            code: 403
          }
        } 
      } else if(err.status === 500) {
        router.navigate(['/error-page'], {
          state: {
            code: 500
          }
        });
      } else if(err.status === 503) {
        router.navigate(['/error-page'], {
          state: {
            code: 503
          }
        });
      }

      return throwError(() => err);
    })
  )
};
